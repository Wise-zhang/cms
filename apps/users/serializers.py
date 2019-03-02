"""

"""
import re

from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from users.models import User, Address


class CreateUserSerializer(serializers.ModelSerializer):
    """校验用户注册信息的序列化器"""
    sms_code = serializers.CharField(label="短信验证码", max_length=6, min_length=6, write_only=True)
    password_2 = serializers.CharField(label="确认密码", write_only=True)
    allow = serializers.BooleanField(label="许可协议", write_only=True)

    # token = serializers.CharField(label="JwtToken", read_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "password_2", "mobile", "sms_code", "allow")

    def validate(self, attrs):
        # 校验短信验证码
        redis_conn = get_redis_connection(alias="verify_codes")  # type: StrictRedis
        sms_code = redis_conn.get("%s_code" % attrs.get("mobile"))
        if not sms_code:
            raise serializers.ValidationError("请先发送短信验证码")
        if sms_code.decode("utf-8") != attrs.get("sms_code"):
            raise serializers.ValidationError("短信验证码错误")
        # 校验两次输入的密码
        if attrs.get("password") != attrs.get("password_2"):
            raise serializers.ValidationError(detail="两次输入的密码不一致")
        # 校验许可协议
        if not attrs.get("allow"):
            raise serializers.ValidationError(detail="请先同意注册许可协议")
        return attrs

    def create(self, validated_data):
        # print(validated_data)
        del validated_data["sms_code"]
        del validated_data["allow"]
        del validated_data["password_2"]

        return super().create(validated_data)


class AddressSer(serializers.ModelSerializer):
    province = StringRelatedField(label="省", read_only=True)
    city = StringRelatedField(label="市", read_only=True)
    district = StringRelatedField(label="省", read_only=True)

    province_id = serializers.IntegerField(label="省id", write_only=True)
    city_id = serializers.IntegerField(label="市id", write_only=True)
    district_id = serializers.IntegerField(label="区id", write_only=True)

    class Meta:
        model = Address
        # fields = '__all__'
        exclude = ('create_time', 'update_time', 'user', 'is_deleted')
        # extra_kwargs = {
        #     "province": {"read_only": True},
        #     "city": {"read_only": True},
        #     "district": {"read_only": True},
        #     # "is_deleted": {"read_only": True},
        # }

    def validate_moble(self, value):
        """验证手机号"""
        if not re.match(r'1[1-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式不对')
        return value

    def create(self, validated_data):
        # validated_datat校验通过的参数
        validated_data["user"] = self.context["request"].user
        # 调用父类方法创建
        return super().create(validated_data)


class UserDefSer(serializers.Serializer):
    default_address_id = serializers.IntegerField(label='默认地址', write_only=True)

    def validate_default_address_id(self, value):
        try:
            Address.objects.get(id=value, user=self.context["request"].user)
        except:
            raise serializers.ValidationError('地市id错误')
        return value

    def update(self, instance, validated_data):
        instance.default_address_id = validated_data['default_address_id']
        instance.save()
        return instance
