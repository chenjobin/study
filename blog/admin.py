from django.contrib import admin

from blog.models import Topic,Entry,Tag


class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_added', 'date_update','owner')
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 15
     #fk_fields 设置显示外键字段
     # fk_fields = ('owner',)
    exclude = ('owner',) #排除该字段
    # 若owner字段为空，则定义owner当前操作的用户
    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','id','author','topic','recommend','date_added', 'date_update')
    list_per_page = 15
    fields = ('topic','title', ('recommend','top_in'),'tags','text')
    list_editable = ['topic', 'recommend']
    # 筛选器
    list_filter =('topic', 'recommend','author__username') # 过滤器
    search_fields =['title'] #搜索字段
    date_hierarchy = 'date_update'    # 详细时间分层筛选
    # 将prepopulated_fields设置为将字段名称映射到其应预先填充的字段的字典：
    # prepopulated_fields = {'author': ('title',)}
    filter_horizontal=('tags',)

    # 若author字段为空，则定义author当前操作的用户
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

admin.site.register(Topic,TopicAdmin)
admin.site.register(Tag)
admin.site.register(Entry,EntryAdmin)