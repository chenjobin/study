from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)

    class Meta:
          ordering = ('name',)
          verbose_name = '产品类目'
          verbose_name_plural = '产品类目'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',verbose_name='产品类目')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 我们总是使用 DecimalField 来保存货币值。 FloatField 在内部使用 Python 的 float 类型。
    # 反之， DecimalField 使用的是 Python 中的 Decimal 类型，使用 Decimal 类型可以避免精度问题。
    stock = models.PositiveIntegerField()   #库存
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])