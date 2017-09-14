from django.shortcuts import render
from .models import Single_Q
from django.http import HttpResponseRedirect,Http404
from django import http
from .models import SingleWrongAnswer

#添加返回json的方法，json结构有3个参数（code:返回码,is_success:是否处理成功,message:消息内容）
def ResponseJson(code, is_success,is_right, message):
    data = {'code':code, 'success':is_success,'right':is_right, 'message':message}
    return http.JsonResponse(data)

def index(request):
    # subjects = Single_Q.objects.all()
    # single_qs = Single_Q.objects.order_by('-date_added')
    # data = {}
    # data['single_qs'] = single_qs
    return render(request,'exam/index.html')

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
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated
    if not user_is_authenticated:
        return ResponseJson(501, False,False, 'No Login')

    answer=data.get('selected','not have a valid value')
    single_q=Single_Q.objects.get(id=selection_id)
    correct_answer=single_q.answer

    # 不管是否答题错误，都将其收入错题集，通过正确次数与错误次数的判断，来进行判定掌握
    try:
        single_wrong=SingleWrongAnswer.objects.filter(user=request.user,question=single_q)
        if not single_wrong.count():
            wrong_q = SingleWrongAnswer(user=request.user,question=single_q)
            wrong_q.save()
            # SingleWrongAnswer.objects.get_or_create(user=request.user,question=single_q,wrong_answer=answer)

        # get方法才可以使 类调用内部函数，filter做不到，所以多弄搞了个single_wrong1
        single_wrong1=SingleWrongAnswer.objects.get(user=request.user,question=single_q)

        if answer==correct_answer:
            if single_wrong1.first_right_times==0:
                single_wrong1.count_first_right_times()
            single_wrong1.increase_correct_times()
            return ResponseJson(200, True, True,'you are right')

        else:
            single_wrong.update(wrong_answer=answer)
            single_wrong1.increase_wrong_times()
            return ResponseJson(200, True, False,answer)
        # else:
        #     return ResponseJson(200, True, False,answer)
    except:
        return ResponseJson(502, False, False,'you are wrong')

