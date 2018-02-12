from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from blog.models import Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.html import format_html

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
    STATUS_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    topic_second = models.ManyToManyField(Exam_Topic_Second,blank=True,verbose_name='归属二级主题')
    # star_it = models.ManyToManyField(User,blank=True,verbose_name='用户收藏')  放在用户那可能更合适
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    # caption = models.CharField('题目简化版',max_length=200)
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')

    answer = models.CharField('正确选项',max_length=10,
                                choices=STATUS_CHOICES,
                                default='')
    # answer = models.CharField('正确选项',max_length=200,default=u'')
    # select_2 = models.CharField('选项2',max_length=200,default=u'')
    # select_3 = models.CharField('选项3',max_length=200,default=u'')
    # select_4 = models.CharField('选项4',max_length=200,default=u'')
    answer_detail = UEditorField('答案解析', height=300, width=1000,
        default=u'略', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')

    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        verbose_name = '单选题'
        verbose_name_plural = '单选题'

    def __str__(self):
        '''返回模型的字符串表示'''
        # if len(self.title)>50:
        #     return format_html(self.title[:50]+'...',)
        # else:
        #     return format_html(self.title,)
        # 发现如果title中如果table，那么会对错题列表造成错误，所以，
        return format_html(self.title,)
    #  admin页面，题目 html代码解析
    def title_format(self):
        return format_html(self.title[:200]+'...',)
    title_format.short_description='题目内容'

# 填空题
class Fill_Q(models.Model):
    '''填空题模型'''
    topic = models.ForeignKey(Exam_Topic,verbose_name='归属主题')
    topic_second = models.ManyToManyField(Exam_Topic_Second,blank=True,verbose_name='归属二级主题')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name='作者')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #多对多字段，绑定下面的Tag模型
    recommend = models.BooleanField('重点题目',default=False) #布尔字段，我用于标记是否是重点题
    # 考虑到HTML的影响，加入简化版，其实是和title一样
    # caption = models.CharField('题目简化版',max_length=200)
    # blank_num=models.PositiveIntegerField(default=1,verbose_name='空白数') # 记录填空的数量
    title = UEditorField('题目', height=300, width=1000,
        default=u'', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')
    answer_detail = UEditorField('答案解析', height=300, width=1000,
        default=u'略', blank=True, imagePath="exam/uploads/images/",
        toolbars='besttome', filePath='exam/uploads/files/')


    date_added = models.DateTimeField('发布时间',auto_now_add=True)
    date_update = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        verbose_name = '填空题'
        verbose_name_plural = '填空题'

    def __str__(self):
        '''返回模型的字符串表示'''
        # if len(self.title)>50:
        #     return format_html(self.title[:50]+'...',)
        # else:
        #     return format_html(self.title,)
        # 发现如果title中如果table，那么会对错题列表造成错误，所以，
        return format_html(self.title,)
    #  admin页面，题目 html代码解析
    def title_format(self):
        return format_html(self.title[:100]+'...',)
    title_format.short_description=u'题目内容'

# 填空题答案
class Fill_Answer(models.Model):
    '''填空题模型答案'''
    fill_q = models.ForeignKey(Fill_Q,verbose_name='归属填空题')
    # 增加属性，区分本题是否为仅有几种有限的答案
    is_only=models.BooleanField('答案形式确定',default=True)
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
    correct_times=models.PositiveIntegerField('答对次数',default=0) # 新增  字段记录正确次数
    wrong_times=models.PositiveIntegerField('错误次数',default=0) # 新增  字段记录错误次数
    first_right_times=models.PositiveIntegerField('第一次做对',default=0) # 第一次答对，是第几次作答

    is_show=models.BooleanField('显示',default=True) #标记该错题是否显示在错题集
    killed_times=models.PositiveIntegerField('斩掉次数',default=1) #斩掉此题次数，提高使之不出现在错题集的权重，

    class Meta:
        verbose_name = '错题本_单选题'
        verbose_name_plural = '错题本_单选题'

    def __str__(self):
        return self.wrong_answer

    def increase_correct_times(self):
        self.correct_times += 1
        # self.show_determine()
        self.save(update_fields=['correct_times'])

    def increase_wrong_times(self):
        self.wrong_times += 1
        # self.show_determine()
        self.save(update_fields=['wrong_times'])

    def increase_killed_times(self):
        self.killed_times += 1
        # self.show_determine()
        self.save(update_fields=['killed_times'])

    def count_first_right_times(self):
        self.first_right_times = self.correct_times + self.wrong_times + 1
        # self.show_determine()
        self.save(update_fields=['first_right_times'])

    def show_determine(self):
        if self.correct_times*self.killed_times>=self.wrong_times:
            self.is_show=False
        # elif self.first_right_times == 1 and self.correct_times>=self.wrong_times:
        #     self.is_show=False
        # elif self.correct_times>=self.wrong_times *2:
        #     self.is_show=False
        else:
            self.is_show=True
        self.save(update_fields=['is_show'])

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
    correct_times=models.PositiveIntegerField('答对次数',default=0) # 新增  字段记录正确次数
    wrong_times=models.PositiveIntegerField('错误次数',default=0) # 新增  字段记录错误次数
    first_right_times=models.PositiveIntegerField('第一次做对',default=0) # 第一次答对，是第几次作答

    is_show=models.BooleanField('显示',default=True) #标记该错题是否显示在错题集
    killed_times=models.PositiveIntegerField('斩掉次数',default=1) #斩掉此题次数，提高使之不出现在错题集的权重，

    class Meta:
        verbose_name = '错题本_填空题'
        verbose_name_plural = '错题本_填空题'

    def __str__(self):
        return self.wrong_answer

    def increase_correct_times(self):
        self.correct_times += 1
        # self.show_determine()
        self.save(update_fields=['correct_times'])

    def increase_wrong_times(self):
        self.wrong_times += 1
        # self.show_determine()
        self.save(update_fields=['wrong_times'])

    def increase_killed_times(self):
        self.killed_times += 1
        # self.show_determine()
        self.save(update_fields=['killed_times'])

    def count_first_right_times(self):
        self.first_right_times = self.correct_times + self.wrong_times + 1
        # self.show_determine()
        self.save(update_fields=['first_right_times'])

    def show_determine(self):
        if self.correct_times*self.killed_times>=self.wrong_times:
            self.is_show=False
        # elif self.first_right_times == 1 and self.correct_times>=self.wrong_times:
        #     self.is_show=False
        # elif self.correct_times>=self.wrong_times *2:
        #     self.is_show=False
        else:
            self.is_show=True
        self.save(update_fields=['is_show'])


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
    title = models.CharField('标题',max_length=250)   #书写模块，本模块答题注意事项
    description = models.TextField('模块描述',max_length=200,default=u'')
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
    question_value = models.PositiveIntegerField('本题分值',default=2)
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

class ExamRecordRound(models.Model):
    '''创建考试场次，以区分各次考试'''
    user = models.ForeignKey(User,verbose_name='创建者')
    title = models.CharField('考试场次',max_length=200,default=u'')
    examination_paper = models.ForeignKey(ExaminationPaper,verbose_name='所属试卷')
    date_begin = models.DateTimeField('考试开始时间')
    date_end = models.DateTimeField('考试结束时间')
    time_limit=models.PositiveIntegerField('考试限制时间（分钟）',default=60)  #单位是分钟

    def __str__(self):
        if len(self.title)>50:
            return self.title[:50] + '...'
        else:
            return self.title[:50]

    class Meta:
        verbose_name = '考试场次'
        verbose_name_plural = '考试场次'

class ExamRecord(models.Model):
    '''考试记录，以区分各次考试'''
    user = models.ForeignKey(User,verbose_name='考生')
    exam_round=models.ForeignKey(ExamRecordRound,verbose_name='考试场次')
    examination_paper = models.ForeignKey(ExaminationPaper,verbose_name='所属试卷')
    date_added = models.DateTimeField('试卷提交时间',auto_now_add=True)

    exam_value = models.PositiveIntegerField('试卷总分值',default=0)
    exam_score = models.PositiveIntegerField('试卷得分',default=0)
    value_single = models.PositiveIntegerField('单选题分值',default=0)
    score_single = models.PositiveIntegerField('单选题得分',default=0)
    value_fill = models.PositiveIntegerField('填空题分值',default=0)
    score_fill = models.PositiveIntegerField('填空题得分',default=0)

    can_reexamine=models.BooleanField('重考',default=False)  #标记该试卷是否可以重考
    reexamine_times = models.PositiveIntegerField('重考次数',default=0)
    reexamine_remark=models.CharField('重考备注',max_length=200,default=u'无')

    class Meta:
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录'

class ExamRecordSingleDetail(models.Model):
    '''考试情况的具体各题目信息'''
    user = models.ForeignKey(User,verbose_name='用户')
    # examination_paper = models.ForeignKey(ExaminationPaper,verbose_name='所属试卷')
    # exam_round=models.ForeignKey(ExamRecordRound,verbose_name='考试场次')
    # 所属考试记录
    exam_record = models.ForeignKey(ExamRecord,verbose_name='所属考试')

    question=models.ForeignKey(Single_Q,verbose_name='题目')
    answer=models.CharField('用户答案',max_length=200,default=u'')
    question_value = models.PositiveIntegerField('本题分值',default=2)
    score=models.PositiveIntegerField('本题得分',default=2)
    is_right=models.BooleanField('正误',default=True)  #标记该题是否答对了

    class Meta:
        verbose_name = '考试记录-单选题'
        verbose_name_plural = '考试记录-单选题'

    def question_format(self):
        return format_html(self.question[:100]+'...',)
    question_format.short_description=u'题目'