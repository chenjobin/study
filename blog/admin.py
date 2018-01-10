from django.contrib import admin

from blog.models import Topic,Entry,Tag


class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_added', 'date_update','owner')
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 15
    #ordering设置默认排序字段，负号表示降序排序
    # ordering = ('text')
    #list_editable 设置默认可编辑字段
    # list_editable = ['text', ]
    #fk_fields 设置显示外键字段
     # fk_fields = ('owner',)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','id','author','topic','recommend','date_added', 'date_update')
    list_per_page = 15
    fields = (('topic', 'author'), 'tags',('recommend','top_in'),'title','text')
    list_editable = ['topic', 'recommend']
    # 筛选器
    list_filter =('topic', 'recommend','author__username') # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_update'    # 详细时间分层筛选
    # 将prepopulated_fields设置为将字段名称映射到其应预先填充的字段的字典：
    # prepopulated_fields = {'author': ('title',)}

admin.site.register(Topic,TopicAdmin)
admin.site.register(Tag)
admin.site.register(Entry,EntryAdmin)