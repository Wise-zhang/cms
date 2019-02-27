"""

"""
from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import serializers

from users.models import User


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
