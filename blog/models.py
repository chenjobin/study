from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 引入这个 Field，其它的不要变
from DjangoUeditor.models import UEditorField


class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    owner=models.ForeignKey(User)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text


class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    topic = models.ForeignKey(Topic)
    text = UEditorField('内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')

    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text)>50:
            return self.text[:50] + '...'
        else:
            return self.text[:50]

