from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 引入这个 Field，其它的不要变
from DjangoUeditor.models import UEditorField
from django.utils.encoding import  python_2_unicode_compatible

@python_2_unicode_compatible
class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField('主题',max_length=200)
    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)
    owner=models.ForeignKey(User,verbose_name='所有者')
    description = models.TextField('相关描述') #描述主题

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

    class Meta:
        verbose_name = '主题' #后台admin  add主题
        verbose_name_plural = '主题'
        # ordering = ['text']  # 按照哪个栏目排序

@python_2_unicode_compatible
class Tag(models.Model):
    """博客分类"""
    tag_name=models.CharField(max_length=20)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

@python_2_unicode_compatible
class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    topic = models.ForeignKey(Topic,verbose_name='归属主题')
    title = models.CharField('标题', max_length=256)
    text = UEditorField('内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True) #多对多字段，绑定下面的Tag模型
    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)
    recommend = models.BooleanField('推荐',default=False) #布尔字段，我用于标记是否是推荐博文
    read_num = models.PositiveIntegerField(default=0) # 新增 views 字段记录阅读量

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text)>50:
            return self.text[:50] + '...'
        else:
            return self.text[:50]

    def increase_read_num(self):
        self.read_num += 1
        self.save(update_fields=['read_num'])
