from django.db import models

from utils.models import Category, Album, BaseModel


class NewsCategory(Category):
    """
    新闻二级分类
    """
    class Meta(object):
        db_table = 't_news_category'
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name


class News(BaseModel):
    """新闻"""

    category = models.ForeignKey('NewsCategory', verbose_name='所属类别')
    title = models.CharField(max_length=100, verbose_name='标题')
    img_url = models.CharField(max_length=255, verbose_name='图片url')
    tags = models.TextField(verbose_name='标识')
    zhaiyao = models.CharField(max_length=255, verbose_name='摘要')
    content = models.TextField(verbose_name = '新闻内容')
    click = models.IntegerField(verbose_name = '点击量')
    status = models.IntegerField(verbose_name = '是否下线')
    is_top = models.IntegerField(verbose_name = '是否头条')
    is_slide = models.IntegerField(verbose_name = '是否轮播新闻')
    source = models.CharField(verbose_name = '新闻来源', max_length=20)
    author = models.CharField(verbose_name = '作者', max_length=20)

    class Meta(object):
        db_table = 't_news'
        verbose_name = '新闻数据'
        verbose_name_plural = verbose_name


class NewsAlbum(Album):
    """新闻图片"""

    # 外键: 所属新闻
    news = models.ForeignKey('News')

    class Meta(object):
        db_table = 't_news_album'
        verbose_name = '新闻图片'
        verbose_name_plural = verbose_name