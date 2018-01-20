from django.contrib import admin
from .models import Subject, Course, Module,Content


# 我们使用@admin.register()装饰器替代了admin.site.register()方法。它们都提供了相同的功能。
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'date_added']
    list_filter = ['date_added', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

    exclude = ('owner',) #排除该字段
    # 若owner字段为空，则定义owner当前操作的用户
    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()
