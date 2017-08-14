from django.contrib import admin

from blog.models import Topic,Entry

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_added', 'date_update','owner')


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','author','topic','date_added', 'date_update',)

admin.site.register(Topic,TopicAdmin)
admin.site.register(Entry,EntryAdmin)