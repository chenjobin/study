'''定义blog的URL模式'''

from django.conf.urls import url

from exam import  views

urlpatterns=[
    #exam主页
    url(r'^exam/$',views.index,name='index'),

]