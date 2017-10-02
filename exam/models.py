from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from blog.models import Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

class Exam_Topic_Second(models.Model):
    '''题目的细分主题'''
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    recommend = models.BooleanField('重要主题',default=False) #布尔字段，标记是否是推荐主题
    caption = models.CharField('二级主题',max_length=200)
    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)
    description = models.TextField('相关描述') #描述主题



    def __str__(self):
        '''返回模型的字符串表示'''
        return self.caption

    class Meta:
        verbose_name = '试题二级分类' #后台admin  add主题
        verbose_name_plural = '试题二级分类'
        # ordering = ['text']  # 按照哪个栏目排序

# 单项选择题
class Single_Q(models.Model):
    '''单选题模型'''
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    topic_second = models.ManyToManyField(Exam_Topic_Second,blank=True,verbose_name='归属二级主题')

    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    caption = models.CharField('题目简化版',max_length=200)
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')
    answer = models.CharField('正确选项',max_length=200,default=u'')
    select_2 = models.CharField('选项2',max_length=200,default=u'')
    select_3 = models.CharField('选项3',max_length=200,default=u'')
    select_4 = models.CharField('选项4',max_length=200,default=u'')
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
    topic_second = models.ManyToManyField(Exam_Topic_Second,blank=True,verbose_name='归属二级主题')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    caption = models.CharField('题目简化版',max_length=200)
    # blank_num=models.PositiveIntegerField(default=1,verbose_name='空白数') # 记录填空的数量
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')
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

# 填空题答案
class Fill_Answer(models.Model):
    '''填空题模型答案'''
    fill_q = models.ForeignKey(Fill_Q,verbose_name='归属填空题')
    # 增加属性，区分本题是否为仅有几种有限的答案
    is_only=models.BooleanField('答案形式确定',default=False)
    # 一般情况下，只有一个answer
    answer1=models.CharField('正确答案1',max_length=200,default=u'')
    answer2=models.CharField('正确答案2',max_length=200,default=u'')
    answer3=models.CharField('正确答案3',max_length=200,default=u'')
    answer4=models.CharField('正确答案4',max_length=200,default=u'')

    class Meta:
        verbose_name = '填空题答案'
        verbose_name_plural = '填空题答案'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.answer1)>50:
            return self.answer1[:50] + '...'
        else:
            return self.answer1[:50]

# 错题表
class SingleWrongAnswer(models.Model):
    '''答错的题目信息'''
    user = models.ForeignKey(User,verbose_name='归属用户')
    question=models.ForeignKey(Single_Q,verbose_name='题目')
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey(
    #     ct_field = "content_type",
    #     fk_field = "object_id"
    # )
    wrong_answer=models.CharField('用户答案',max_length=200,default=u'')
    date_update = models.DateTimeField('更新时间',auto_now=True)

    # 进入错题集后，若是正确次数>5,且正确/错误 大于3，表明已基本掌握本题
    correct_times=models.PositiveIntegerField('第一次做对',default=0) # 新增  字段记录正确次数
    wrong_times=models.PositiveIntegerField('错误次数',default=0) # 新增  字段记录错误次数
    first_right_times=models.PositiveIntegerField('答对次数',default=0) # 第一次答对，是第几次作答

    class Meta:
        verbose_name = '错题本_单选题'
        verbose_name_plural = '错题本_单选题'

    def __str__(self):
        return self.wrong_answer

    def increase_correct_times(self):
        self.correct_times += 1
        self.save(update_fields=['correct_times'])

    def increase_wrong_times(self):
        self.wrong_times += 1
        self.save(update_fields=['wrong_times'])

    def count_first_right_times(self):
        self.first_right_times = self.correct_times + self.wrong_times + 1
        self.save(update_fields=['first_right_times'])

# 错题表 填空题
# 相对照于选择题错题集，此题仅多了一个wrong_fill_n字段，以后可以考虑错题集使用同一个模型
class FillWrongAnswer(models.Model):
    '''答错的题目信息'''
    user = models.ForeignKey(User,verbose_name='归属用户')
    question=models.ForeignKey(Fill_Q,verbose_name='题目')
    # 记录第几个空答错了,
    # 这么做,以后填空题错题提取的时候要注意去重了
    wrong_fill_n=models.PositiveIntegerField(default=0)

    wrong_answer=models.CharField('用户答案',max_length=200,default=u'')
    date_update = models.DateTimeField('更新时间',auto_now=True)

    # 进入错题集后，若是正确次数>5,且正确/错误 大于3，表明已基本掌握本题
    correct_times=models.PositiveIntegerField('第一次做对',default=0) # 新增  字段记录正确次数
    wrong_times=models.PositiveIntegerField('错误次数',default=0) # 新增  字段记录错误次数
    first_right_times=models.PositiveIntegerField('答对次数',default=0) # 第一次答对，是第几次作答

    class Meta:
        verbose_name = '错题本_填空题'
        verbose_name_plural = '错题本_填空题'

    def __str__(self):
        return self.wrong_answer

    def increase_correct_times(self):
        self.correct_times += 1
        self.save(update_fields=['correct_times'])

    def increase_wrong_times(self):
        self.wrong_times += 1
        self.save(update_fields=['wrong_times'])

    def count_first_right_times(self):
        self.first_right_times = self.correct_times + self.wrong_times + 1
        self.save(update_fields=['first_right_times'])


class ExaminationPaperType(models.Model):
    '''subject type'''
    type_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.type_name)

    class Meta:
        verbose_name = '试卷类型'
        verbose_name_plural = '试卷类型'


class ExaminationPaper(models.Model):
    '''subject model'''
    caption = models.CharField(max_length=20)
    description = models.TextField()

    author = models.ForeignKey(User, default=1)
    # 模拟卷 真题卷
    exam_paper_type = models.ForeignKey(ExaminationPaperType, default=1)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.caption

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'


class ExaminationPaperChapter(models.Model):
    '''ExaminationPaper chapter
        用来划分第一部分第二部分，也可以理解成划分选择题填空题
    '''
    title = models.CharField(max_length=250)   #书写模块，本模块答题注意事项
    examination_paper = models.ForeignKey(ExaminationPaper)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'<%s-%s>' % (self.title, self.examination_paper)

    class Meta:
        verbose_name = '试卷模块'
        verbose_name_plural = '试卷模块'

class ExaminationPaperItem(models.Model):
    '''subject item'''
    chapter = models.ForeignKey(ExaminationPaperChapter, default=1)

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
        verbose_name = '试卷具体试题'
        verbose_name_plural = '试卷具体试题'