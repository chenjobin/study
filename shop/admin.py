from django.contrib import admin

from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock',
                    'available', 'date_added', 'date_update']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    # 筛选
    list_filter = ['available', 'date_added', 'date_update']
    search_fields =['name'] #搜索所属试卷caption字段
    date_hierarchy = 'date_update'    # 按试卷创建时间分层筛选

admin.site.register(Product, ProductAdmin)
