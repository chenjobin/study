from django.shortcuts import render
from .models import Single_Q
from django.http import HttpResponseRedirect,Http404
from django import http

#添加返回json的方法，json结构有3个参数（code:返回码,is_success:是否处理成功,message:消息内容）
def ResponseJson(code, is_success,is_right, message):
    data = {'code':code, 'success':is_success,'right':is_right, 'message':message}
    return http.JsonResponse(data)

def index(request):
    # subjects = Single_Q.objects.all()
    single_qs = Single_Q.objects.order_by('-date_added')
    data = {}
    data['single_qs'] = single_qs
    return render(request,'exam/index.html', data)

def selection(request):
    # subjects = Single_Q.objects.all()
    single_qs = Single_Q.objects.order_by('-date_added')
    data = {}
    data['single_qs'] = single_qs
    return render(request,'exam/selection.html', data)

def detail_selection(request,selection_id):
    try:
        single_q=Single_Q.objects.get(id=selection_id)
        topic=single_q.topic

        # 获取前后各一篇博文,QuerySet的写法，毕竟SQL查询可读性不强,所以没有使用。
        #__gt和__lt分别是大于和小于的意思。可以修饰到判断条件的字段上
        next_single_q = Single_Q.objects.filter(id__gt=selection_id).order_by('id')
        pre_single_q = Single_Q.objects.filter(id__lt=selection_id).order_by('-id')

        #取第1条记录
        if pre_single_q.count() > 0:
            pre_single_q = pre_single_q[0]
        else:
            pre_single_q = None

        if next_single_q.count() > 0:
            next_single_q = next_single_q[0]
        else:
            next_single_q = None

        context={'topic':topic,'single_q':single_q,'pre_single_q':pre_single_q,'next_single_q':next_single_q}
    except Single_Q.DoesNotExist:
        raise Http404
    return render(request,'exam/detail_selection.html',context)

def selection_check_answer(request,selection_id):
    data = request.POST.copy()
    # try:
    #     user_is_authenticated = request.user.is_authenticated()
    # except TypeError:  # Django >= 1.11
    #     user_is_authenticated = request.user.is_authenticated
    # if user_is_authenticated:
    #     if not data.get('name', ''):
    #         data["name"] = request.user.get_short_name() or request.user.get_username()
    #     if not data.get('email', ''):
    #         data["email"] = request.user.email
    # else:
    #     return ResponseJson(501, False, 'No Login')
    try:
        answer=data.get('selected','not have a valid value')
        single_q=Single_Q.objects.get(id=selection_id)
        correct_answer=single_q.answer
    except:
        return ResponseJson(501, False, False,'can\'t find the answer')

    if answer==correct_answer:
        return ResponseJson(200, True, True,'you are right')
    else:
        return ResponseJson(200, True, False,answer)
        # return ResponseJson(200, True, False,'you are wrong')
