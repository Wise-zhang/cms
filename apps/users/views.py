import random
import re

from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import serializers as s
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, UpdateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from celery_tasks.sms.tasks import send_sms_code
from users import serializers

from users.models import User, Address
from users.serializers import CreateUserSerializer


class ValidateNameView(APIView):
    """校验用户名"""

    def post(self, request):
        username = request.data.get("username")
        user = User.objects.filter(username=username).all()
        if user:
            raise s.ValidationError(detail="重复的用户名！")
        return Response(data={"messages": "用户名可用！"})


class SendMobileCodeView(APIView):
    """发送短信验证码"""

    def post(self, request):
        # 校验手机号码
        mobile = request.data.get("mobile")
        mobile = re.match("1[3-9][0-9]{9}$", mobile)
        if not mobile:
            return Response(data={"code": "400", "messages": "手机号码格式错误"})
        mobile = mobile.group()
        # 查询手机号是否被注册
        user = User.objects.filter(mobile=mobile)
        if user:
            return Response(data={"messages": "手机号码已经被注册"})
        # 校验是否频繁发送
        redis_conn = get_redis_connection(alias="verify_codes")  # type:StrictRedis
        send_flag = redis_conn.get("%s_flag" % mobile)
        if send_flag:
            # 短信验证码存在
            return Response(data={"messages": "请求频繁"})

        sms_code = redis_conn.get("%s_code" % mobile)
        if not sms_code:
            # 生成新的短信验证码
            sms_code = "%06d" % random.randint(0, 999999)
            # 存储验证码到redis数据库
            redis_conn.set("%s_code" % mobile, sms_code, ex=60 * 5)
        else:
            sms_code = sms_code.decode("utf-8")

        redis_conn.set("%s_flag" % mobile, 1, ex=60)  # 一分钟后自动清除
        # 7.执行异步任务发送验证码
        send_sms_code.delay(mobile, sms_code)
        print(sms_code)

        return Response(data={"messages": "短信验证码发送成功"})


class RegisterView(CreateAPIView):
    """注册用户"""
    serializer_class = CreateUserSerializer


class LoginView(APIView):
    """登录视图"""

    def post(self, request):
        """
        1. 获取前端传的用户密码
        2. 通过用户名查询出用户名是否存在
            1. 不存在返回错误提示：用户名未注册
        3. 校验密码是否正确
        """
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={"status": 400, "messages": "用户名未注册"}, status=200)
        if password != user.password:
            return Response(data={"status": 400, "messages": "账号或密码错误"}, status=200)

        # 生成JWT的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {
            "status": 200,
            "id": user.id,
            "username": username,
            "token": token
        }
        return Response(data=data)


class AddressView(ListCreateAPIView):
    """新增、查询多地址"""
    serializer_class = serializers.AddressSer

    # 默认
    # pagination_class = None
    # 可以通过重写获取queryset
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializers = self.get_serializer(queryset, many=True)
        return Response({"addresses": serializers.data, "default_address_id": request.user.default_address_id})


class DelAddressView(RetrieveDestroyAPIView):
    serializer_class = serializers.AddressSer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class DefAddressView(UpdateAPIView):
    serializer_class = serializers.UserDefSer

    def get_object(self):
        return self.request.user
