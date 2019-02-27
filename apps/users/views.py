import random
import re

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from users.models import User


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

        return Response(data={"messages": "短信验证码发送成功"})
