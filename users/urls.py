'''定义users的URL模式'''
from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    #登录页面
    url(r'^login/$',login,{'template_name':'users/login.html'},name='login'),
    #注销页面
    url(r'^logout/$',views.logout_view,name='logout'),
    #注册页面
    url(r'^register/$',views.register,name='register'),

    url(r'^user_active/([a-zA-Z]+)$',views.user_active,name='user_active'),
]
