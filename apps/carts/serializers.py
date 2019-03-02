from rest_framework import serializers

from goods.models import Goods


class CartSerializer(serializers.Serializer):
    """
    需要校验的数据有 sku_id count selected
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


class CartGoodsSerializer(serializers.ModelSerializer):
    # 增加两个序列化的字段
    count = serializers.IntegerField(label='数量', min_value=1)
    select = serializers.BooleanField(label='是否勾选', default=False)

    class Meta:   # 元类
        model = Goods
        fields = ('id', 'count', 'title', 'img_url', 'sell_price', 'select')


class CartDeleteSerializer(serializers.Serializer):
    """删除商品序列化器"""
    sku_id = serializers.IntegerField(label='商品id', min_value=1)

    def validated_sku_id(self, value):
        try:
            sku = Goods.objects.get(id=value)

        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value


class CartSelectSerializer(serializers.Serializer):
    select = serializers.BooleanField(label="全选")