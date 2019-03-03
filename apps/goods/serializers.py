from rest_framework.serializers import ModelSerializer

from goods.models import Goods, GoodsCategory, GoodsAlbum


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'img_url', 'title', 'sub_title', 'create_time', 'sell_price')


class SubCategory(ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title',)
class PareCategory(ModelSerializer):
    parent=SubCategory(read_only=True)
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title','parent')


class CategorySerializer(ModelSerializer):
    goodscategory_set = SubCategory(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'goodscategory_set')


class GoodListSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'img_url', 'title', 'market_price', 'stock', 'sell_price')


class GoodsAlbumSerializer(ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = ('id', 'thumb_path', 'original_path')


class GoodDetailSerializer(ModelSerializer):
    goodsalbum_set = GoodsAlbumSerializer(many=True, read_only=True)
    category=PareCategory(read_only=True)
    class Meta:
        model = Goods
        fields = ('id', 'img_url', 'title', 'market_price', 'stock', 'sell_price', 'goods_no', 'sub_title', 'goodsalbum_set','category')



class RecommendGoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'img_url', 'title', 'create_time')
