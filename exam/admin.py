from django.contrib import admin
from .models import Exam_Topic,Exam_Topic_Second,Single_Q,Fill_Q,Fill_Answer,SingleWrongAnswer,FillWrongAnswer,\
    ExaminationPaperType,ExaminationPaper,ExaminationPaperChapter,ExaminationPaperItem

class Exam_TopicAdmin(admin.ModelAdmin):
    list_display = ('caption','id','date_added', 'date_update')
    # list_per_page = 15
    # fields = (('topic', 'author'), 'tags',('recommend','top_in'),'title','text')

class Exam_Topic_SecondAdmin(admin.ModelAdmin):
    list_display = ('caption','id','topic','date_added', 'date_update','recommend')
    # list_per_page = 15
    fields = (('topic', 'recommend'), 'caption','description')

class Single_QAdmin(admin.ModelAdmin):
    list_display = ('caption','id','author','topic','date_added', 'date_update','recommend')
    list_per_page = 15
    fields = (('topic', 'author','recommend'),( 'topic_second','tags'),'caption','title',
              'answer',('select_2','select_3','select_4'),'answer_detail')

class Fill_AnswerInline(admin.TabularInline):
    model = Fill_Answer
    extra = 3

class Fill_QAdmin(admin.ModelAdmin):
    list_display = ('caption','author','id','topic','date_added', 'date_update','recommend')
    list_per_page = 15
    fields = (('topic', 'author','recommend'), ( 'topic_second','tags'),'caption','title','answer_detail')
    inlines=[Fill_AnswerInline]

class SingleWrongAnswerAdmin(admin.ModelAdmin):
    list_display = ('question','user','first_right_times','correct_times','wrong_times')

class FillWrongAnswerAdmin(admin.ModelAdmin):
    list_display = ('question','user','wrong_fill_n','first_right_times','correct_times','wrong_times')

# 试卷分类
class ExaminationPaperTypeAdmin(admin.ModelAdmin):
    list_display=('id', 'type_name', 'create_time')

#试卷 部分
class ExaminationPaperChapterInline(admin.TabularInline):
    model = ExaminationPaperChapter
    extra = 3
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

admin.site.register(Exam_Topic,Exam_TopicAdmin)
admin.site.register(Exam_Topic_Second,Exam_Topic_SecondAdmin)
admin.site.register(Single_Q,Single_QAdmin)
admin.site.register(Fill_Q,Fill_QAdmin)
admin.site.register(SingleWrongAnswer,SingleWrongAnswerAdmin)
admin.site.register(FillWrongAnswer,FillWrongAnswerAdmin)

admin.site.register(ExaminationPaperType,ExaminationPaperTypeAdmin)
admin.site.register(ExaminationPaper,ExaminationPaperAdmin)
admin.site.register(ExaminationPaperChapter,ExaminationPaperChapterAdmin)

