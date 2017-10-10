from django.shortcuts import render
from .models import Single_Q,Fill_Q
from django.http import HttpResponseRedirect,Http404
from django import http
from .models import SingleWrongAnswer,FillWrongAnswer,ExaminationPaper
from django.core.urlresolvers import reverse #url逆向解析

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

def fill_question(request):
    # subjects = Single_Q.objects.all()
    fill_qs = Fill_Q.objects.order_by('-date_added')
    data = {}
    data['fill_qs'] = fill_qs
    return render(request,'exam/fill_question.html', data)

def exam_paper(request):
    # subjects = Single_Q.objects.all()
    exam_papers = ExaminationPaper.objects.order_by('-create_time')
    data = {}
    data['exam_papers'] = exam_papers
    return render(request,'exam/exam_paper_list.html', data)

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

def single_check(request,selection_id):
    data = request.POST.copy()
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated
    if not user_is_authenticated:
        return ResponseJson(501, False,False, 'No Login')

    answer=data.get('selected','not have a valid value')
    right_wrong=[]
    try:
        context=single_check_answer(request,answer,selection_id)
        right_wrong.append(context)
        return ResponseJson(200, True, right_wrong,[233,1333])
    except:
        return ResponseJson(502, False, False,'you are wrong')

def detail_fill(request,fill_q_id):
    try:
        fill_q=Fill_Q.objects.get(id=fill_q_id)
        topic=fill_q.topic
        # 增加一个空格数
        blank_num=fill_q.fill_answer_set.count()
        #将空格数变成一个list,方便前端遍历
        fill_q.blank_nums=range(1,blank_num+1)
        # for fill_question in fill_q.fill_answer_set.all():
        #     fill_q.blank_num+=1

        # 获取前后各一篇博文,QuerySet的写法，毕竟SQL查询可读性不强,所以没有使用。
        #__gt和__lt分别是大于和小于的意思。可以修饰到判断条件的字段上
        next_fill_q = Fill_Q.objects.filter(id__gt=fill_q_id).order_by('id')
        pre_fill_q = Fill_Q.objects.filter(id__lt=fill_q_id).order_by('-id')

        #取第1条记录
        if pre_fill_q.count() > 0:
            pre_fill_q = pre_fill_q[0]
        else:
            pre_fill_q = None

        if next_fill_q.count() > 0:
            next_fill_q = next_fill_q[0]
        else:
            next_fill_q = None

        context={'topic':topic,'fill_q':fill_q,'pre_fill_q':pre_fill_q,'next_fill_q':next_fill_q}
    except Fill_Q.DoesNotExist:
        raise Http404
    return render(request,'exam/detail_fill.html',context)

def fill_check(request,fill_q_id):
    data = request.POST.copy()
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated
    if not user_is_authenticated:
        return ResponseJson(501, False,False, 'No Login')

    fill_answers=data.getlist('fill_qs')

    # if fill_answers:
    #     return ResponseJson(200, True, True,fill_answers)
    try:
        right_wrong=[True] #第一个True在前端不被考虑进答案的对错，因为前端的i不能+1，所以
        # context_n_list是同一个id几个空的列表，id一样，因为exam部分需要用到n_list,所以用了
        context,context_n_list=fill_check_answer(request,fill_answers,fill_q_id)
        # 因为此处context返回的是list,所以用 + 进行连接
        right_wrong = right_wrong + context

        return ResponseJson(200, True, right_wrong,right_wrong)
    except:
        return ResponseJson(502, False, False,'you are wrong')

def exam_paper_show(request, exam_paper_id):
    try:
        exam_paper = ExaminationPaper.objects.get(id=exam_paper_id)
        chapters = []
        #数据统计
        single_q_num = 0
        fill_q_num = 0
        # temp_j是为了前端第1题到第17题附加导航正常显示
        temp_quest_number=0
        #遍历章节
        for i, chapter in enumerate(exam_paper.examinationpaperchapter_set.all()):
            #遍历子项
            items = []
            for item in chapter.examinationpaperitem_set.all():
                obj = item.content_type.get_object_for_this_type(id=item.object_id)
                obj_type = item.content_type.model

                #根据类型不同，设置名称和链接（动态绑定属性）
                if obj_type == 'single_q':
                    item.type_name = '单选题'
                    # item.url = reverse('exam:detail_selection', args = [item.object_id,])
                    single_q_selections=Single_Q.objects.get(id=item.object_id)
                    item.select_answers = []
                    item.select_answers.append(single_q_selections.answer)
                    item.select_answers.append(single_q_selections.select_2)
                    item.select_answers.append(single_q_selections.select_3)
                    item.select_answers.append(single_q_selections.select_4)

                    item.title = obj.title
                    item.answer = obj.answer
                    single_q_num += 1
                elif obj_type == 'fill_q':
                    item.type_name = '填空题'
                    # item.url = reverse('exam:detail_fill', args = [item.object_id,])
                    fill_answers = Fill_Q.objects.get(id=item.object_id)
                    # 增加一个空格数
                    blank_num=fill_answers.fill_answer_set.count()
                    #将空格数变成一个list,方便前端遍历
                    item.blank_nums=range(1,blank_num+1)
                    item.title = obj.title
                    fill_q_num += 1
                else:
                    item.type_name = '未知'
                    # item.url = '/'
                    item.title = '<未知的类型>'
                temp_quest_number += 1
                item.quest_number = temp_quest_number
                items.append(item)

            chapter.items = items
            chapter.sort_num = i + 1
            chapters.append(chapter)

    except ExaminationPaper.DoesNotExist:
        raise Http404

    data = {}
    data['exam_paper'] = exam_paper
    data['chapters'] = chapters
    data['count'] = u'该试卷分%s部分，共%s道选择题、%s道填空题' % (len(chapters), single_q_num, fill_q_num)

    return render(request,'exam/exam_paper.html', data)

def exam_check(request):
    data = request.POST.copy()
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated
    if not user_is_authenticated:
        return ResponseJson(501, False,False, 'No Login')

    answers=data.getlist('selected','not have a valid value')
    single_q_ids=data.getlist('selected_id')

    fill_answers=data.getlist('fill_qs')
    # 搜集每一个空的题目id 和 该空是属于本题第几空
    fill_q_ids=data.getlist('fill_q_id')
    fill_q_ns=data.getlist('fill_q_n')
    # 弄一个去重的fill_q_ids
    news_ids = []
    for id in fill_q_ids:
        if id not in news_ids:
            news_ids.append(id)

    #第一个True 和 2 在前端不被考虑进答案的对错，因为前端的i不能+1，所以
    right_wrong=[True]
    right_wrong_id_list=[2]

    try:
        # 判断选择题
        for single_q_id,answer in zip(single_q_ids,answers):
            # pass
            context=single_check_answer(request,answer,single_q_id)
            right_wrong.append(context)
            right_wrong_id_list.append(single_q_id)

        # 判断填空题
        i=0     #i和j用来标记fill_answers的起始，也就是找到对应id的对应answer
        j=0
        for fill_q_id in news_ids:
            i = j
            j = j + fill_q_ids.count(fill_q_id)
            context,context_n_list=fill_check_answer(request,fill_answers[i:j],fill_q_id)
            # 因为此处context返回的是list,所以用 + 进行连接
            right_wrong = right_wrong + context
            right_wrong_id_list = right_wrong_id_list + context_n_list


        # for fill_q_id,fill_q_n in zip(fill_answers,fill_q_ids,fill_q_ns):
        #     # pass
        #     context=fill_check_answer(request,fill_answers,fill_q_id)
        #     # 因为此处context返回的是list,所以用 + 进行连接
        #     right_wrong = right_wrong + context

        return ResponseJson(200, True, right_wrong,right_wrong_id_list)
    except:
        return ResponseJson(502, False, False,'you are wrong')

# 单选题答案验证，OK
def single_check_answer(request,answer,single_q_id):
    single_q=Single_Q.objects.get(id=single_q_id)
    correct_answer=single_q.answer

    # 不管是否答题错误，都将其收入错题集，通过正确次数与错误次数的判断，来进行判定掌握
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
        return True

    else:
        single_wrong.update(wrong_answer=answer)
        single_wrong1.increase_wrong_times()
        return False

def fill_check_answer(request,fill_q_answers,fill_q_id):
    '''填空题答案验证'''
    fill_q=Fill_Q.objects.get(id=fill_q_id)
    correct_answer=[]
    right_wrong=[]
    context_n_list=[]
    # obj = answer_item.content_type.get_object_for_this_type(id=answer_item.object_id)
    for i,answer_item in enumerate(fill_q.fill_answer_set.all()):

        # 不管是否答题错误，都将其收入错题集，通过正确次数与错误次数的判断，来进行判定掌握
        # 若以后错题集模型合并，可以考虑一下函数抽象出来
        fill_wrong=FillWrongAnswer.objects.filter(user=request.user,question=fill_q,wrong_fill_n=i+1)
        if not fill_wrong.count():
            wrong_q = FillWrongAnswer(user=request.user,question=fill_q,wrong_fill_n=i+1)
            wrong_q.save()

         # get方法才可以使 类调用内部函数，filter做不到，所以多弄搞了个fill_wrong1
        fill_wrong1=FillWrongAnswer.objects.get(user=request.user,question=fill_q,wrong_fill_n=i+1)

        correct_answer.append(answer_item.answer1)
        # 同一空下，答案的四种可能性
        current_correct_answer=[]
        current_correct_answer.append(answer_item.answer1)
        current_correct_answer.append(answer_item.answer2)
        current_correct_answer.append(answer_item.answer3)
        current_correct_answer.append(answer_item.answer4)
        # 去除字符串空格，避免因空格而弄错
        # 考虑到编程题中，字符串中间可能需要空格，所以，不对中间的空格进行考虑去除
        # 但又考虑编程题中间可能出现2个空格，决定还是对空格进行过滤
        current_correct_answer[0]=''.join(current_correct_answer[0].split())
        current_correct_answer[1]=''.join(current_correct_answer[1].split())
        current_correct_answer[2]=''.join(current_correct_answer[2].split())
        current_correct_answer[3]=''.join(current_correct_answer[3].split())
        fill_q_answers[i]=''.join(fill_q_answers[i].split())

        if fill_q_answers[i]==current_correct_answer[0] \
                or fill_q_answers[i]==current_correct_answer[1] \
                or fill_q_answers[i]==current_correct_answer[2] \
                or fill_q_answers[i]==current_correct_answer[3]:
            right_wrong.append(True)
            context_n_list.append('fill_q_'+ fill_q_id + '_' + str(i+1))
            if fill_wrong1.first_right_times==0:
                fill_wrong1.count_first_right_times()
            fill_wrong1.increase_correct_times()
        else:
            right_wrong.append(False)
            context_n_list.append('fill_q_'+ fill_q_id + '_' + str(i+1))
            fill_wrong1.increase_wrong_times()
            fill_wrong.update(wrong_answer=fill_q_answers[i])
            # pass
    # if right_wrong[0]==True:
    #     return ResponseJson(200, True, True,correct_answer)
    # else:
    #     return ResponseJson(200, True, False,correct_answer)
    # 收入错题集，如果没有全部答对

    return right_wrong,context_n_list

