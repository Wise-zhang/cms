from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


from news import serializers
from news.models import News


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
