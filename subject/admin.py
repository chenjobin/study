from django.contrib import admin
from .models import SubjectType, SubjectStaticType, Subject, SubjectChapter, SubjectItem

#辅助部分
@admin.register(SubjectType)
class SubjectTypeAdmin(admin.ModelAdmin):
    list_display=('id', 'type_name', 'create_time')

@admin.register(SubjectStaticType)
class SubjectStaticTypeAdmin(admin.ModelAdmin):
    list_display=('id', 'type_name', 'create_time')

#Subject部分
class SubjectChapterInline(admin.TabularInline):
    model = SubjectChapter
    extra = 3

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=('caption', 'description', 'subject_type', 'static', 'create_time', 'update_time')
    inlines = [SubjectChapterInline,]

#Subject章节
class SubjectItemInline(admin.TabularInline):
    model = SubjectItem
    extra = 3

@admin.register(SubjectChapter)
class SubjectChapterAdmin(admin.ModelAdmin):
    list_display=('subject', 'title', 'create_time')
    # 筛选器
    search_fields =['subject__caption'] #搜索所属专题caption字段
    date_hierarchy = 'subject__create_time'    # 按专题创建时间分层筛选

    inlines = [SubjectItemInline,]