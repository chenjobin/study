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

    url(r'^post/(?P<selection_id>\d+)$',views.single_check,name='single_check'),

    # 填空题页
    url(r'^fill_question/$',views.fill_question,name='fill_question'),
    # 填空题详细页
    url(r'^detail_fill/(?P<fill_q_id>\d+)$',views.detail_fill,name='detail_fill'),

    url(r'^post2/(?P<fill_q_id>\d+)$',views.fill_check,name='fill_check'),

    # 整卷显示，仿专题
    url(r'^exam_paper/$',views.exam_paper,name='exam_paper'),
    url(r'^exam_paper/(?P<exam_paper_id>\d+)/$',views.exam_paper_show,name='exam_paper_show'),
    url(r'^post3/$',views.exam_check,name='exam_check'),

    # 错题集
    url(r'^single_wrong/$',views.single_wrong,name='single_wrong'),
    url(r'^detail_single_wrong/(?P<single_q_id>\d+),(?P<single_wrong_q_id>\d+)$',views.detail_single_wrong,name='detail_single_wrong'),
]