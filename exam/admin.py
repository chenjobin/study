from django.contrib import admin
from .models import Exam_Topic,Single_Q

class Exam_TopicAdmin(admin.ModelAdmin):
    list_display = ('caption','id','date_added', 'date_update')
    # list_per_page = 15
    # fields = (('topic', 'author'), 'tags',('recommend','top_in'),'title','text')


class Single_QAdmin(admin.ModelAdmin):
    list_display = ('caption','id','author','topic','date_added', 'date_update','recommend')
    list_per_page = 15
    fields = (('topic', 'author','recommend'), 'tags','caption','title','answer_detail',
              'select_correct',('select_2','select_3','select_4'))


admin.site.register(Exam_Topic,Exam_TopicAdmin)
admin.site.register(Single_Q,Single_QAdmin)