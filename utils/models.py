from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class Category(BaseModel):
    """多级分类(针对新闻, 商品等频道),目前只用到了1,2两个频道"""
    title = models.CharField(max_length=100, verbose_name='类别名称')
    sort_id = models.IntegerField(verbose_name='排序权重')
    parent = models.ForeignKey('self', verbose_name='父类别')

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class Album(BaseModel):
    """
    组图,相册
    """
    thumb_path = models.CharField(max_length=255, verbose_name='缩略图url')
    original_path = models.CharField(max_length=255, verbose_name='原图url')
    remark = models.TextField(verbose_name='备注信息', null=True)

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True
