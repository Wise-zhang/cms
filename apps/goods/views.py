from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsCategory, Goods
from goods.serializers import GoodsSerializer, CategorySerializer, GoodListSerializer, GoodDetailSerializer, \
    RecommendGoodsSerializer, PareCategory


class GoodsIndexTopView(APIView):
    """
    商城首页上端显示视图
    """

    def get(self, request):
        top_dict = {}
        # 轮播图商品
        slide_queryset = Goods.objects.filter(is_slide=1, status=0).all()
        ser = GoodsSerializer(instance=slide_queryset, many=True)
        top_dict['slide_goods'] = ser.data
        # 推荐商品
        recommend_queryset = Goods.objects.filter(is_red=1, status=0).all()[0:4]
        ser = GoodsSerializer(instance=recommend_queryset, many=True)
        top_dict['recommend_goods'] = ser.data
        # 商品分类
        category_queryset = GoodsCategory.objects.filter(parent_id=0).all()
        ser = CategorySerializer(instance=category_queryset, many=True)
        top_dict['category_goods'] = ser.data
        return Response(top_dict)


class GoodsIndexSubView(APIView):
    """
    商城首页下端显示视图
    """

    def get(self, request):
        # 一级分类
        category_queryset = GoodsCategory.objects.filter(parent_id=0).all()
        print(len(category_queryset))
        data_list = []
        for category in category_queryset:
            # 一级分类
            data_dict = CategorySerializer(instance=category).data
            # 获得属于该一级分类下的所有二级分类的id
            sub_list = category.goodscategory_set.all()
            id_list = []
            for sub in sub_list:
                id_list.append(sub.id)
            # 属于该一级分类的商品
            good_queryset = Goods.objects.filter(category_id__in=id_list, status=0).all()
            data_dict['goods'] = GoodsSerializer(instance=good_queryset, many=True).data
            data_list.append(data_dict)
        return Response(data_list)


class GoodsListView(ListAPIView):
    """
    查询分类商品的列表
    """

    # serializer_class = GoodListSerializer
    #
    # def get_queryset(self):
    #     category = int(self.request.data['category'])
    #     cate = GoodsCategory.objects.get(category)
    #     if cate.parent_id == 0:
    #         sub_list = cate.goodscategory_set.all()
    #         id_list = []
    #         for sub in sub_list:
    #             id_list.append(sub.id)
    #         # 属于该一级分类的商品
    #         return Goods.objects.filter(category_id__in=id_list).all()
    #
    #     else:
    #         return Goods.objects.filter(category_id=category).all()
    filter_backends = [OrderingFilter]
    ordering_fields = ('sales', 'stock', 'sell_price')
    serializer_class = GoodListSerializer

    def get_queryset(self):
        category = self.request.query_params['category']
        cate = GoodsCategory.objects.get(id=category)
        if cate.parent_id == 0:
            sub_list = cate.goodscategory_set.all()
            id_list = []
            for sub in sub_list:
                id_list.append(sub.id)
            # 属于该一级分类的商品
            good_query = Goods.objects.filter(category_id__in=id_list, status=0).all()

        else:
            good_query = Goods.objects.filter(category_id=category, status=0).all()
        return good_query


class GoodsDetailView(RetrieveAPIView):
    """
    商品详情页商品详细信息视图
    """
    serializer_class = GoodDetailSerializer
    queryset = Goods.objects.all()


class RecommendGoodsView(ListAPIView):
    """
    商品详情页推荐商品视图
    """
    serializer_class = RecommendGoodsSerializer
    queryset = Goods.objects.filter(is_red=1, status=0).all()[0:4]


class NavView(APIView):
    """
    根据商品ID查询父分类
    """

    def get(self, request, pk):
        goods = Goods.objects.get(id=pk)
        category = goods.category.title  # 当前商品的类别
        category_id = goods.category.id  # 当前商品的类别

        parent = GoodsCategory.objects.get(id=category_id)
        parent_title = parent.parent.title
        parent_id = parent.parent.id

        data = {
            "current": {
                "id": category_id,
                "title": category,
            },
            "parent": {
                "id": parent_id,
                "title": parent_title,
            }
        }

        return Response(data=data)


class ListNavView(APIView):
    def get(self, request):
        category_id = request.query_params['category_id']
        category = GoodsCategory.objects.get(id=category_id)
        serializer = PareCategory(instance=category)
        return Response(serializer.data)


