from rest_framework.serializers import ModelSerializer

from news.models import News

class NewsTopSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
