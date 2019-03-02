from rest_framework.serializers import ModelSerializer

from news.models import News, NewsCategory


class NewsTopSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class SonNewsCateSerializer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'title')


class NewsCateSerializer(ModelSerializer):
    newscategory_set = SonNewsCateSerializer(many=True, read_only=True)

    class Meta:
        model = NewsCategory
        fields = ('id', 'title', 'newscategory_set')
