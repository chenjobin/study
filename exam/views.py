from django.shortcuts import render
from .models import Single_Q
from django.http import HttpResponseRedirect,Http404

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