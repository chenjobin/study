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

    # 填空题页
    url(r'^fill_question/$',views.fill_question,name='fill_question'),
    # 填空题详细页
    url(r'^detail_fill/(?P<fill_q_id>\d+)$',views.detail_fill,name='detail_fill'),

    url(r'^post2/(?P<fill_q_id>\d+)$',views.fill_check_answer,name='fill_check_answer'),

    # 整卷显示，仿专题
    url(r'^exam_paper/$',views.exam_paper,name='exam_paper'),
    url(r'^exam_paper/(?P<exam_paper_id>\d+)/$',views.exam_paper_show,name='exam_paper_show'),
]