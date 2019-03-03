from django.db import models

from utils.models import Category, BaseModel, Album


class GoodsCategory(Category):
    """
    新闻多级分类
    """
    title = models.CharField(max_length=100, verbose_name='类别名称')
    sort_id = models.IntegerField(verbose_name='排序权重')
    parent = models.ForeignKey('self', verbose_name='父类别')
    class Meta(object):
        db_table = 't_goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """商品表"""

    category = models.ForeignKey('GoodsCategory', verbose_name='类别')
    title = models.CharField(max_length=100, verbose_name='商品名称')
    img_url = models.CharField(max_length=255, verbose_name='商品默认图片')
    zhaiyao = models.CharField(max_length=255, verbose_name='摘要')
    content = models.TextField(default='', verbose_name='商品详情')
    status = models.IntegerField(default=0, verbose_name='是否下线')
    is_red = models.IntegerField(default=0, verbose_name='是否推荐')
    is_slide = models.IntegerField(default=0, verbose_name='是否轮播商品')
    sub_title = models.CharField(max_length=255, verbose_name='子标题')
    goods_no = models.CharField(max_length=100, verbose_name='商品编号')
    stock = models.IntegerField(verbose_name='商品库存')
    sales = models.IntegerField(verbose_name='销量')
    market_price = models.DecimalField(max_digits=9, decimal_places=2,
                                       verbose_name='市场价')
    sell_price = models.DecimalField(max_digits=9, decimal_places=2,
                                     verbose_name='销售价')

    class Meta(object):
        db_table = 't_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class GoodsAlbum(Album):
    """商品图片"""

    # 所属商品
    goods = models.ForeignKey('Goods')

    class Meta(object):
        db_table = 't_goods_album'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
