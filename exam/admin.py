from django.contrib import admin
from .models import Exam_Topic,Exam_Topic_Second,Single_Q,Fill_Q,Fill_Answer,SingleWrongAnswer,FillWrongAnswer,\
    ExaminationPaperType,ExaminationPaper,ExaminationPaperChapter,ExaminationPaperItem,\
    ExamRecordRound,ExamRecordSingleDetail,ExamRecord,ExamRecordFillDetail

class Exam_TopicAdmin(admin.ModelAdmin):
    list_display = ('caption','id','date_added', 'date_update')
    # list_per_page = 15
    # fields = (('topic', 'author'), 'tags',('recommend','top_in'),'title','text')

class Exam_Topic_SecondAdmin(admin.ModelAdmin):
    list_display = ('caption','id','topic','date_added', 'date_update','recommend')
    # list_per_page = 15
    fields = (('topic', 'recommend'), 'caption','description')

class Single_QAdmin(admin.ModelAdmin):
    list_display = ('title_format','id','topic','author','recommend','date_added')
    list_per_page = 15
    fields = (('topic','recommend'),'topic_second','tags','title',
              'answer','answer_detail')
    list_editable = ['topic', 'recommend']
    # 筛选器
    list_filter =('topic', 'recommend','author__username') # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_added'    # 详细时间分层筛选

    filter_horizontal=('topic_second','tags')

    # 若author字段为空，则定义author当前操作的用户
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class Fill_AnswerInline(admin.TabularInline):
    model = Fill_Answer
    extra = 3

class Fill_QAdmin(admin.ModelAdmin):
    list_display = ('title_format','id','topic','author','recommend','date_added')
    list_per_page = 15
    fields = (('topic','recommend'), 'topic_second','tags','title','answer_detail')
    list_editable = ['topic', 'recommend']
    # 筛选器
    list_filter =('topic', 'recommend','author__username') # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_added'    # 详细时间分层筛选

    filter_horizontal=('topic_second','tags')

    inlines=[Fill_AnswerInline]

    # 若author字段为空，则定义author当前操作的用户
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class SingleWrongAnswerAdmin(admin.ModelAdmin):
    list_display = ('question','user','first_right_times','correct_times','wrong_times')
    # 筛选器
    list_filter =['user__username'] # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_update'    # 详细时间分层筛选

class FillWrongAnswerAdmin(admin.ModelAdmin):
    list_display = ('question','user','wrong_fill_n','first_right_times','correct_times','wrong_times')
    # 筛选器
    list_filter =['user__username'] # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_update'    # 详细时间分层筛选

# 试卷分类
class ExaminationPaperTypeAdmin(admin.ModelAdmin):
    list_display=('id', 'type_name', 'create_time')

#试卷 部分 class ExaminationPaperChapterInline(admin.TabularInline): 界面会紧凑些
class ExaminationPaperChapterInline(admin.StackedInline):
    model = ExaminationPaperChapter
    extra = 1
# 试卷
class ExaminationPaperAdmin(admin.ModelAdmin):
    list_display=('caption', 'description', 'exam_paper_type','create_time', 'update_time')
    inlines = [ExaminationPaperChapterInline,]

#试卷 各 模块
class ExaminationPaperItemInline(admin.TabularInline):
    model = ExaminationPaperItem
    extra = 3

class ExaminationPaperChapterAdmin(admin.ModelAdmin):
    list_display=('examination_paper', 'title', 'create_time')
    inlines = [ExaminationPaperItemInline,]
    # 筛选器
    list_filter =('examination_paper__exam_paper_type', ) # 以试卷类型作为过滤器
    search_fields =['examination_paper__caption'] #搜索所属试卷caption字段
    date_hierarchy = 'examination_paper__create_time'    # 按试卷创建时间分层筛选

admin.site.register(Exam_Topic,Exam_TopicAdmin)
admin.site.register(Exam_Topic_Second,Exam_Topic_SecondAdmin)
admin.site.register(Single_Q,Single_QAdmin)
admin.site.register(Fill_Q,Fill_QAdmin)
admin.site.register(SingleWrongAnswer,SingleWrongAnswerAdmin)
admin.site.register(FillWrongAnswer,FillWrongAnswerAdmin)

admin.site.register(ExaminationPaperType,ExaminationPaperTypeAdmin)
admin.site.register(ExaminationPaper,ExaminationPaperAdmin)
admin.site.register(ExaminationPaperChapter,ExaminationPaperChapterAdmin)

# 我们使用@admin.register()装饰器替代了admin.site.register()方法。它们都提供了相同的功能。
# 考试场次
@admin.register(ExamRecordRound)
class ExamRecordRoundAdmin(admin.ModelAdmin):
    list_display = ['title', 'examination_paper','date_begin','time_limit','user']

# 考试记录 总括
@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ['exam_round','examination_paper','user', 'exam_value','exam_score','value_single','score_single',
                    'value_fill','score_fill','reexamine_times']

    fields = ['exam_round','examination_paper','user', ('exam_value','exam_score'),
                    ('value_single','score_single'),('value_fill','score_fill'),'reexamine_times',
              ('can_reexamine','reexamine_remark')]

# 考试记录 单选题
@admin.register(ExamRecordSingleDetail)
class ExamRecordSingleDetailAdmin(admin.ModelAdmin):
    list_display = ['user','exam_record','question_value','score','answer','is_right','question']

# 考试记录 填空题
@admin.register(ExamRecordFillDetail)
class ExamRecordFillDetailAdmin(admin.ModelAdmin):
    list_display = ['user','exam_record','question_value','fill_n','score','answer','is_right','question']
