from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField   #导入定制字段
from django.template.loader import render_to_string
# 渲染不同类型的内容
from django.utils.safestring import mark_safe

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ('title',)
    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,blank=True, null=True, verbose_name='作者',
                                 related_name='courses_created')
    subject = models.ForeignKey(Subject,
                                   related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 添加学生
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)

    class Meta:
        ordering = ('-date_added',)
    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    order = OrderField(blank=True, for_fields=['course'])   #使用定制字段

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents')
    # content_type = models.ForeignKey(ContentType)
    # 添加一个limit_choices_to参数来限制ContentType对象可以被通用关系使用
    content_type = models.ForeignKey(ContentType,
                      limit_choices_to={'model__in':('text',
                                           'video',
                                           'image',
                                           'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    order = OrderField(blank=True, for_fields=['module'])   #使用定制字段

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related')
    # 我们使用%(class)s_related作为related_name，给子模型的相对关系将各自是text_related,file_related,image_related,以及video_related
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    # 渲染不同类型的内容
    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})

class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()


