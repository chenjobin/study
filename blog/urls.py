'''定义blog的URL模式'''

from django.conf.urls import url

from . import  views

urlpatterns=[
    #主页
    url(r'^$',views.index,name='index'),
    #博客主页
    url(r'^blog/$',views.index1,name='index1'),
    url(r'^blog_list/$',views.blog_list,name='blog_list'),

    #显示所有的主题
    url(r'^topics/$',views.topics,name='topics'),
    #推荐博文
    url(r'^recommends/$',views.entry_recommend,name='recommends'),

    #特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    url(r'^tag/(?P<tag_id>\d+)$',views.tag,name='tag'),

    #用于添加新主题的网页
    url(r'^new_topic/$',views.new_topic,name='new_topic'),

    #用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$',views.new_entry,name='new_entry'),

    #用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),

    #用于详细条目内容的页面
    url(r'^detail_entry/(?P<entry_id>\d+)/$',views.detail_entry,name='detail_entry'),

    #搜索框
    url(r'^search/$',views.search,name='search'),
]