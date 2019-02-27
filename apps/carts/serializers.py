from rest_framework import serializers

from goods.models import Goods


class CartSerializer(serializers.Serializer):
    """
    需要校验的数据有 sku_id count select
    """
    sku_id = serializers.IntegerField(label='商品id', min_value=1)
    count = serializers.IntegerField(label='数量', min_value=1)
    select = serializers.BooleanField(label='是否勾选', default=False)

    def validate(self, attrs):
        try:
            sku = Goods.objects.get(id=attrs['sku_id'])
        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return attrs     # 这里必须返回校验数据