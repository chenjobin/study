from django.contrib import admin
from .models import Exam_Topic,Single_Q,Fill_Q,Fill_Answer

class Exam_TopicAdmin(admin.ModelAdmin):
    list_display = ('caption','id','date_added', 'date_update')
    # list_per_page = 15
    # fields = (('topic', 'author'), 'tags',('recommend','top_in'),'title','text')


class Single_QAdmin(admin.ModelAdmin):
    list_display = ('caption','id','author','topic','date_added', 'date_update','recommend')
    list_per_page = 15
    fields = (('topic', 'author','recommend'), 'tags','caption','title',
              'answer',('select_2','select_3','select_4'),'answer_detail')

class Fill_AnswerInline(admin.TabularInline):
    model = Fill_Answer
    extra = 3

class Fill_QAdmin(admin.ModelAdmin):
    list_display = ('caption','id','author','topic','date_added', 'date_update','recommend')
    list_per_page = 15
    fields = (('topic', 'author','recommend'), 'tags',('caption','blank_num'),'title','answer_detail')
    inlines=[Fill_AnswerInline]

admin.site.register(Exam_Topic,Exam_TopicAdmin)
admin.site.register(Single_Q,Single_QAdmin)
admin.site.register(Fill_Q,Fill_QAdmin)