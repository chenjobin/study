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

    url(r'^user_info$',views.user_info,name='user_info'),

    url(r'^nickname_change$',views.nickname_change,name='nickname_change'),

    url(r'^password_change$',views.password_change,name='password_change'),
    # 密码找回
    url(r'password_lost', views.password_lost, name='password_lost'),
    url(r'get_email_code', views.get_email_code, name='get_email_code'),
    # 修改头像
    url(r'avatar_change', views.avatar_change, name='avatar_change'),
]
