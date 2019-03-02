from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from news import serializers
from news.models import News, NewsCategory


class NewsTopView(APIView):
    def get(self, request):
        # slide_news: [],
        # top_news: [],
        # image_news: [],

        # 轮播图新闻
        slide_news = News.objects.filter(is_slide=True).exclude(img_url='')

        # 推荐新闻
        top_news = News.objects.order_by('-create_time')[0:10]
        # 图片新闻
        image_news = News.objects.exclude(img_url='').order_by('-create_time')[0:4]

        slide_news = serializers.NewsTopSerializer(slide_news, many=True).data
        top_news = serializers.NewsTopSerializer(top_news, many=True).data
        image_news = serializers.NewsTopSerializer(image_news, many=True).data
        data = {
            "slide_news": slide_news,
            "top_news": top_news,
            "image_news": image_news,
        }
        return Response(data)


class NewsCateView(APIView):
    def get(self, request):
        # 一级类别
        cate_queryset = NewsCategory.objects.filter(parent_id=0).all()
        # 用于存放返回数据
        data_list = []
        for cate in cate_queryset:
            # 序列化一级分类新闻
            cate_dict = serializers.NewsCateSerializer(cate).data
            # 获取二级分类
            son_cate_list = cate.newscategory_set.all()
            # 存放二级新闻id
            son_id_list = []
            for son_cate in son_cate_list:
                son_id_list.append(son_cate.id)
            cate_dict['news'] = serializers.NewsTopSerializer(
                News.objects.filter(category_id__in=son_id_list).exclude(img_url='').order_by('-create_time')[0:4],
                many=True).data
            cate_dict['top8'] = serializers.NewsTopSerializer(
                News.objects.filter(category_id__in=son_id_list).order_by('-click')[0:8], many=True).data
            data_list.append(cate_dict)
        return Response(data_list)
