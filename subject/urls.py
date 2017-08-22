'''定义blog的URL模式'''

from django.conf.urls import url

from . import  views

urlpatterns=[

    url(r'^subject/$',views.subject_list,name='subject_list'),

    url(r'^subject/(?P<subject_id>\d+)/$',views.subject_show,name='subject_show'),

]