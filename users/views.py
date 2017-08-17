from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm
from django.contrib.auth.models import User

def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

def register(request):
    '''注册新用户'''
    if request.method !='POST':
        #显示空的注册表单
        form = RegisterForm()
    else:
        #处理填写好的表单
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            # new_user=form.save()
            #让用户自动登录，再重定向到主页
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('blog:index'))

    context={'form':form}
    return render(request,'users/register.html',context)