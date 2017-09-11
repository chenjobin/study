'''定义blog的URL模式'''

from django.conf.urls import url

from exam import  views

urlpatterns=[
    #exam主页
    url(r'^exam/$',views.index,name='index'),
    # 选择题页
    url(r'^selection/$',views.selection,name='selection'),
    # 选择题详细页
    url(r'^detail_selection/(?P<selection_id>\d+)$',views.detail_selection,name='detail_selection'),

    url(r'^post/(?P<selection_id>\d+)$',views.selection_check_answer,name='selection_check_answer'),
]