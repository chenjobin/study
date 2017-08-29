from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.utils.encoding import  python_2_unicode_compatible
from blog.models import Tag


@python_2_unicode_compatible
class Exam_Topic(models.Model):
    '''题目的主题'''
    caption = models.CharField('主题',max_length=200)
    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)
    description = models.TextField('相关描述') #描述主题

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.caption

    class Meta:
        verbose_name = '试题分类' #后台admin  add主题
        verbose_name_plural = '试题分类'
        # ordering = ['text']  # 按照哪个栏目排序

# 单项选择题
class Single_Q(models.Model):
    '''单选题模型'''
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    caption = models.CharField('题目简化版',max_length=200)
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')
    answer = models.TextField('正确选项',max_length=200,default=u'')
    select_2 = models.TextField('选项2',max_length=200,default=u'')
    select_3 = models.TextField('选项3',max_length=200,default=u'')
    select_4 = models.TextField('选项4',max_length=200,default=u'')
    answer_detail = UEditorField('答案解析', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')

    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        verbose_name = '单选题'
        verbose_name_plural = '单选题'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.caption)>50:
            return self.caption[:50] + '...'
        else:
            return self.caption[:50]

# 填空题
class Fill_Q(models.Model):
    '''填空题模型'''
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    caption = models.CharField('题目简化版',max_length=200)
    blank_num=models.PositiveIntegerField(default=1,verbose_name='空白数') # 记录填空的数量
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')
    answer=models.TextField('正确答案',max_length=200,default=u'')
    answer_detail = UEditorField('答案解析', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')


    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        verbose_name = '填空题'
        verbose_name_plural = '填空题'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.caption)>50:
            return self.caption[:50] + '...'
        else:
            return self.caption[:50]

