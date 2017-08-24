from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
import django_comments

class SubjectType(models.Model):
    '''subject type'''
    type_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.type_name)

    class Meta:
        verbose_name = '专题类别'
        verbose_name_plural = '专题类别'


class SubjectStaticType(models.Model):
    '''subject static type'''
    type_name = models.CharField(max_length = 12)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '专题类别状态'
        verbose_name_plural = '专题类别状态'


class Subject(models.Model):
    '''subject model'''
    caption = models.CharField(max_length=20)
    description = models.TextField()

    author = models.ForeignKey(User, default=1)
    img = models.FileField(upload_to='subject')
    static = models.ForeignKey(SubjectStaticType, default=1)
    subject_type = models.ForeignKey(SubjectType, default=1)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    read_num = models.PositiveIntegerField(default=0) # 新增 字段记录阅读量

    def __str__(self):
        return '%s' % self.caption

    class Meta:
        verbose_name = '专题'
        verbose_name_plural = '专题'

    #获取评论和回复数
    def get_comment_count(self):
        obj_type = ContentType.objects.get_for_model(self)
        comment_model = django_comments.get_model()
        comments = comment_model.objects.filter(content_type=obj_type, object_pk=self.id)
        return comments.count()

    def increase_read_num(self):
        self.read_num += 1
        self.save(update_fields=['read_num'])

class SubjectChapter(models.Model):
    '''subject chapter'''
    title = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'<%s-%s>' % (self.title, self.subject)

    class Meta:
        verbose_name = '专题章节'
        verbose_name_plural = '专题章节'

class SubjectItem(models.Model):
    '''subject item'''
    chapter = models.ForeignKey(SubjectChapter, default=1)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field = "content_type",
        fk_field = "object_id"
    )

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'subject item %s' % self.id

    class Meta:
        verbose_name = '专题文章'
        verbose_name_plural = '专题文章'
