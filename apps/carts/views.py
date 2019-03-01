import base64

import pickle
from django.shortcuts import render
from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer, CartGoodsSerializer, CartDeleteSerializer
from goods.models import Goods


class CartView(APIView):
    """
    无论登不登陆都可以进行增删改查购物车商品
    """
    def perform_authentication(self, request):
        """
        这个函数主要是为了解决：用户未登录时，添加购物车报错的问题
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        # drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        # 如果认证不通过, 则会抛异常返回401状态码
        # 抛异常会导致视图无法执行，可以在此处捕获异常
        try:
            super().perform_authentication(request)   # 此方法是父类APIView的方法
        except Exception as e:
            print("错误信息error", e)

    def post(self, request):
        """添加购物车"""
        # 校验传过来的参数是否合法
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 新增对象的话这个是必须的

        # 获取序列化后返回的对象

        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        # 保存用户的购物车选择
        user = request.user  # 用户都可以从request里获取
        if user.is_authenticated():  # 判断是否已登录
            # 用户已登录，在redis中保存
            redis_conn = get_redis_connection('cart')  # type:StrictRedis
            pl = redis_conn.pipeline()  # 管道操作提高性能
            # 增加购物车商品数量
            pl.hincrby('cart_%s' % user.id, sku_id, count)
            if selected:  # 保存商品勾选状态
                pl.sadd('cart_selected_%s' % user.id, sku_id)
            pl.execute()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 未登陆情况下保存在cookies中,前端只考虑登陆状态下
        # else:
        #     # 1. 从cookie中获取购物车信息  <--用户未登录页让他加入购物车
        #     cart = request.COOKIES.get('cart')  # 从cookie中获取信息   后端生成
        #     # cart 字典类型
        #     # 2. base64字符串
        #     if cart is not None:
        #         # pickle.loads() 将bytes类型数据反序列化为python的数据类型
        #         cart = pickle.loads(base64.b64decode(cart.encode()))
        #     else:
        #         cart = {}
        #
        #     # 3. 新增字典中对应的商品数量
        #     # print(cart)
        #     # {1: {'count': 3, 'selected': True}, 15: {'count': 2, 'selected': True}}
        #     sku = cart.get(sku_id)
        #     # print(sku)
        #     # {'count': 2, 'selected': True}
        #     if sku:  # 原有数量 + 新增数量  --》就是数据覆盖1
        #         count += int(sku.get('count'))
        #     cart[sku_id] = {
        #         'count': count,
        #         'selected': selected
        #     }
        #
        #     # 4. 字典 --> base64字符串
        #     cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
        #
        #     # 5. 通过cookie保存购物车数据（base64字符串）
        #     response = Response(serializer.data, status=201)
        #     # 参数3： cookie有效期
        #     response.set_cookie('cart', cookie_cart, 30*24*3600)
        #     return response

    def get(self, request):
        """获取用户购物车所有的商品"""
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            dict_cart = redis_conn.hgetall('cart_%s' % user.id)  # cart_1 = {1: 2， 2：2}
            list_cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)  # cart_selected_1 = {1}   这里应该是元组

            # 拼装字典 cart_1 = {1: 2， 2：2}   cart_selected_1 = {1}
            # {1:{'count':2, 'selected':False}, 2:{'count':2, 'selected':False}}
            cart = {}
            # 把redis中所有的hush和set中的全部数据查出来便利组装到一个字典中

            # sku_id:{'count':count,'selected':False}
            for sku_id, count in dict_cart.items():
                cart[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in list_cart_selected  # 相当于布尔值 不是对就是错
                }
            # 查询数据库数据返回序列化后的数据
            # 查询购物车中所有的商品  cart.keys() cart中所有的键
            skus = Goods.objects.filter(id__in=cart.keys())  # 得到的是查询集
            for sku in skus:  # 数据库查询到的是没有count和selected这两个字段的，手动添加
                # 给sku对象新增两个字段: 商品数量和勾选状态
                sku.count = cart[sku.id]['count']
                sku.selected = cart[sku.id]['selected']

            # 序列化操作
            serializer = CartGoodsSerializer(skus, many=True)
            print(serializer.data)
            return Response(serializer.data)

    def delete(self, request):

        serializer = CartDeleteSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        # 获取sku_id
        sku_id = serializer.validated_data.get('sku_id')
        user = request.user
        if user.is_authenticated:
            # 获取用户要删除的商品id
            # 用户已登录，在redis中保存
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            pl.hdel('cart_%s' % user.id, sku_id)
            pl.srem('cart_selected_%s' % user.id, sku_id)
            pl.execute()
            return Response(status=status.HTTP_204_NO_CONTENT)


