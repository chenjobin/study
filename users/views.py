from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout,authenticate
# from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm,ChangeNickForm,ChangePwdForm,ForgetPwdForm,ChangAvatarForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives   #发送邮件
from my_plug import comments_count

import json, time, datetime, random, string,re
from .models import User_ex
from django.utils import timezone

def logout_view(request):
    '''注销用户'''
    #记住来源的url，如果没有则设置为首页('/')
    returnPath=request.META.get('HTTP_REFERER', '/')
    logout(request)
    # return HttpResponseRedirect(reverse('blog:index'))
    return HttpResponseRedirect(returnPath)


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
            # 判断注册邮箱是否已经存在
            is_exist = User.objects.filter(email=email).count()>0

            if is_exist:
                response_data={'success': u'sorry,注册失败,此邮箱已被使用，This Email has been used'}
                return JsonResponse(response_data)
            else:
                new_user = User.objects.create_user(username, email, password)
                new_user.is_active = False
                new_user.save()

                    #发送激活邮件
                    #不想用uuid模块生成唯一ID保存到数据库中，也不想用django-registration
                    #安全级别要求不高，所以简单写个加密解密的方法来处理
                active_code=get_active_code(email)
                send_active_email(email,active_code)

                # new_user=form.save()
                #让用户自动登录，再重定向到主页
                # authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
                # login(request,authenticated_user)
                # return HttpResponseRedirect(reverse('blog:index'))
                response_data={'success': u'注册成功,请前往邮箱激活后登录,Check Email to Active your account'}
                return JsonResponse(response_data)

    context={'form':form}
    return render(request,'users/register.html',context)

def get_active_code(email):
    """get active code by email and current date"""
    key=9
    encry_str='%s|%s' % (email,time.strftime('%Y-%m-%d',time.localtime(time.time())))
    active_code=encrypt(key,encry_str)
    return active_code

def send_active_email(email,active_code):
    """send the active email"""
    # url='http://127.0.0.1:8000%s' % (reverse('users:user_active',args=(active_code,)))
    url='http://chenzhibin.vip%s' % (reverse('users:user_active',args=(active_code,)))

    subject=u'[chenzhibin.vip]激活您的帐号'
    message=u'''
        <h2>陈志斌的博客(<a href="http://chenzhibin.vip/" target=_blank>chenzhibin.vip</a>)<h2><br />
        <p>欢迎注册，请点击下面链接进行激活操作(7天后过期)：<a href="%s" target=_blank>%s</a></p>
        ''' % (url,url)

    send_to=[email]
    fail_silently=True  #发送异常不报错

    msg=EmailMultiAlternatives(subject=subject,body=message,to=send_to)
    msg.attach_alternative(message, "text/html")
    msg.send(fail_silently)

def encrypt(key, s):
    """encrypt string(key is a number)"""
    b = bytearray(str(s).encode('utf-8'))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode('utf-8').lower()

def decrypt(key, s):
    """decrypt string(key is a number)"""
    c = bytearray(str(s).upper().encode('utf-8'))
    n = len(c) # 计算 b 的字节数
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode('utf-8')
    except:
        return ""

def user_active(request,active_code):
    """user active from the code"""
    #加错误处理，避免出错。出错认为激活链接失效
    #解密激活链接
    key=9
    data={}
    try:
        decrypt_str=decrypt(key,active_code)
        decrypt_data=decrypt_str.split('|')
        email=decrypt_data[0]                                   #邮箱
        create_date=time.strptime(decrypt_data[1], "%Y-%m-%d")  #激活链接创建日期
        create_date=time.mktime(create_date)            #struct_time 转成浮点型的时间戳

        day=int((time.time()-create_date)/(24*60*60))     #得到日期差
        if day>7:
            raise Exception(u'激活链接过期')

        #激活
        user=User.objects.filter(email=email)
        if len(user)==0:
            raise Exception(u'user0激活链接无效')
        else:
            user=User.objects.get(email=email)

        if user.is_active:
            raise Exception(u'该帐号已激活过了')
        else:
            user.is_active=True
            user.save()

        data['goto_page']=True
        data['message']=u'激活成功，欢迎访问！'
    except IndexError as e:
        data['goto_page']=False
        data['message']=u'激活链接无效'
    except Exception as e:
        data['goto_page']=False
        data['message']=e
    finally:
        #激活成功就跳转到首页(message页面有自动跳转功能)
        data['goto_url']='/'
        data['goto_time']=3000
        return render_to_response('message.html',data)

#添加用户中心的响应方法
def user_info(request):
    '''show the user infomations'''
    data={}
    user = request.user
    #判断是否登录了
    if request.user.is_authenticated():
        data['user'] = user
        data['comments_count'] = comments_count.get_comments_count(user.id)
        data['replies_count'] = comments_count.get_replies_count(user.id)
        data['replyed_count'] = comments_count.get_to_reply_count(user.id)
        data['last_talk_about'] = comments_count.last_talk_about(user.id)
        data['all_talk_about'] = comments_count.all_talk_about(user.id)
        return render_to_response('users/index.html',data)
    else:
        data['message'] = u'您尚未登录，请先登录' #提示消息
        data['goto_page'] = True #是否跳转
        data['goto_url'] = '/'  #跳转页面
        data['goto_time'] = 3000  #等待多久才跳转
        return render_to_response('message.html',data)

#装饰器，登录判断
def check_login(func):
    def wrapper(request):
        #登录判断，若没登录则跳转到前面写的信息提示页面
        if not request.user.is_authenticated():
            data = {}
            data['goto_url'] = '/'
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'您尚未登录，请先登录'
            return render_to_response('message.html',data)
        else:
            return func(request)
    return wrapper

@check_login
def nickname_change(request):
    data = {}
    data['form_title'] = u'修改昵称'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ChangeNickForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            nickname = form.cleaned_data['nickname']
            request.user.first_name = nickname
            request.user.save()

            #页面提示
            data['goto_url'] = reverse('users:user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'修改昵称成功，修改为“%s”' % nickname
            return render_to_response('message.html',data)
    else:
        #正常加载
        nickname = request.user.first_name or request.user.username
        #用initial给表单填写初始值
        form = ChangeNickForm(initial={
            'old_nickname': nickname,
            'nickname': nickname,
            })
    data['form'] = form
    return render(request, 'users/nickname_or_password_change.html', data)

@check_login
def password_change(request):
    data = {}
    data['form_title'] = u'修改密码'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ChangePwdForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            username = request.user.username
            pwd = form.cleaned_data['pwd_2']
            request.user.set_password(pwd)
            request.user.save()

            #重新登录
            user = authenticate(username=username, password=pwd)
            if user is not None:
                login(request, user)

            #页面提示
            data['goto_url'] = reverse('users:user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'修改密码成功，请牢记新密码'
            return render_to_response('message.html',data)
    else:
        #正常加载
        username = request.user.username
        form = ChangePwdForm(initial={'username':username})
    data['form'] = form
    return render(request, 'users/nickname_or_password_change.html', data)

#  get_email_code(request):两个为用户忘记密码时候，找回密码所用
def password_lost(request):
    """forgot password deals"""
    data = {}
    data['form_title'] = u'重置密码'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ForgetPwdForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd_2']
            user = User.objects.get(email = email)
            user.set_password(pwd)
            user.save()

            #删除验证码
            ex = User_ex.objects.filter(user=user)
            if ex.count() > 0:
                ex.delete()

            #如果是未激活账户找回密码，则发送激活邮件
            if user.is_active == 0:
                active_code=get_active_code(email)
                send_active_email(email,active_code)

            #重新登录
            user = authenticate(username=user.username, password=pwd)
            if user is not None:
                login(request, user)

            #页面提示
            data['goto_url'] = reverse('users:user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'重置密码成功，请牢记新密码'
            return render_to_response('message.html',data)
    else:
        #正常加载
        form = ForgetPwdForm()
    data['form'] = form
    return render(request, 'users/pwd_forget.html', data)

def get_email_code(request):
    """get email code"""
    email = request.GET.get('email', '')
    # 验证码生成，原先的用了就不行，原因以后再看
    # code = ''.join(random.sample(string.digits + string.letters, 6))
    code=generate_verification_code()

    data = {}
    data['success'] = False
    data['message'] = ''

    try:
        #检查邮箱
        users = User.objects.filter(email = email)
        if len(users)==0:
            data['success'] = False
            data['message'] = u'此邮箱未注册'
            # raise Exception, data['message']
            raise Exception(data['message'])

        user = users[0]

        #检查短时间内是否有生成过验证码
        user_ex = User_ex.objects.filter(user = user)
        if len(user_ex)>0:
            user_ex = user_ex[0]

            #两个datetime相减，得到datetime.timedelta类型
            create_time = user_ex.valid_time
            td = timezone.now() - create_time
            if td.seconds < 60:
                data['message'] = u'1分钟内发送过一次验证码'
                # raise Exception, data['message']
                raise Exception(data['message'])
        else:
            #没有则新建
            user_ex = User_ex(user = user)

        #写入数据库
        user_ex.valid_code = code
        user_ex.valid_time = timezone.now()
        user_ex.save()

        #发送邮件
        subject=u'[chenzhibin.vip]重置您的帐号'
        message=u"""
            <h2>陈志斌的博客(<a href='http://chenzhibin.vip/' target=_blank>chenzbibin.vip</a>)<h2><br />
            <p>重置密码的验证码(有效期10分钟)：%s</p>
            <p><br/>(请保管好您的验证码)</p>
            """ % code

        send_to=[email]
        fail_silently=True  #发送异常不报错

        msg=EmailMultiAlternatives(subject=subject,body=message,to=send_to)
        msg.attach_alternative(message, "text/html")
        msg.send(fail_silently)

        data['success'] = True
        data['message'] = 'OK'
    except Exception as e:
        pass
    finally:
        return JsonResponse(data)
        # return HttpResponse(json.dumps(data), content_type="application/json")

def generate_verification_code():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(10): # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91): # A-Z
        code_list.append(chr(i))
    for i in range(97, 123): # a-z
        code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice) # list to string
    # print code_list
    # print type(myslice)
    return verification_code

#几乎原封不动引用了昵称修改的方法，考虑到以后更换用户系统，所以就这样先把
def avatar_change(request):
    data = {}
    data['form_title'] = u'修改头像'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ChangAvatarForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            nickname = form.cleaned_data['nickname']
            request.user.last_name = nickname
            request.user.save()

            #页面提示
            data['goto_url'] = reverse('users:user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'修改头像成功，修改为“%s”' % nickname
            return render_to_response('message.html',data)
    else:
        #正常加载
        nickname = request.user.last_name
        #用initial给表单填写初始值
        form = ChangAvatarForm(initial={
            'old_nickname': nickname,
            'nickname': nickname,
            })
    data['form'] = form
    return render(request, 'users/avatar.html', data)