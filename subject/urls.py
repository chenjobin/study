'''定义blog的URL模式'''

from django.conf.urls import url

from . import  views

urlpatterns=[

    url(r'^subject/$',views.index,name='index'),

    url(r'^subject/(?P<subject_id>\d+)/$',views.subject_show,name='subject_show'),

]