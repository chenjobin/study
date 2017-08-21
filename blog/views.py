from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry,Tag
from .forms import TopicForm,EntryForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.core.mail import send_mail #导入django发送邮件模块
from django.db.models.aggregates import Count

# Create your views here.
def index(request):
    '''网站主页'''
    # return render(request,'blog/index.html') # 制作多个项目时，index,base等放templates根目录
    tags=Tag.objects.order_by('date_added')
    context={'tags':tags}
    return render(request,'index.html',context)

def index1(request):
    '''Blog的主页'''
    # topics=Topic.objects.order_by('date_added')
    # topic.entry_set.count模板中使用该方法也可以获得该topic的文章数量，但是每次执行都会调用一次数据库
    # 使用annotate 仅调用一次数据库
    # 这里 annotate 不仅从数据库获取了全部分类，相当于使用了 all 方法，
    # 它还帮我们为每一个分类添加了一个 num_entry 属性，其值为该分类下的文章数，这样我们在模板中就可以调用这个属性
    topics = Topic.objects.annotate(num_entry=Count('entry'))
    # 计算Entry的数量
    entries_num=Entry.objects.count()
    entries_recommend=Entry.objects.filter(recommend=1).count() #获取推荐文章数量
    context={'topics':topics,'entries_num':entries_num,'entries_recommend':entries_recommend}
    return render(request,'blog/index.html',context)

def tag(request,tag_id):
    '''显示特定tag及其所有的条目'''
    limit = 7  # 每页显示的记录数
    tag=Tag.objects.get(id=tag_id)

    entries=tag.entry_set.order_by('-date_added')

    pages,entries=getPages(request,entries)  #将Paginator封装成函数了

    context={'tag':tag,'entries':entries,'pages':pages}
    return render(request,'blog/tag.html',context)

# @login_required
def topics(request):
    '''显示所有的主题'''
    # topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    topics=Topic.objects.order_by('date_added')
    context={'topics':topics}
    return render(request,'blog/topics.html',context)

# @login_required
def topic(request,topic_id):
    '''显示特定主题及其所有的条目'''
    limit = 7  # 每页显示的记录数
    topic=Topic.objects.get(id=topic_id)
    #确认请求的主题属于当前用户
    # if topic.owner !=request.user:
    #     raise Http404

    entries=topic.entry_set.order_by('-date_added')
    # pages = Paginator(entries, limit)  # 实例化一个分页对象
    #
    # page = request.GET.get('page',1)  # 获取GET请求的参数，得到当前页码。若没有该参数，默认为1
    # try:
    #     entries = pages.page(page)  # 获取某页对应的记录
    # except PageNotAnInteger:  # 如果页码不是个整数
    #     entries = pages.page(1)  # 取第一页的记录
    # except EmptyPage:  # 如果页码太大，没有相应的记录
    #     entries = pages.page(pages.num_pages)  # 取最后一页的记录
    pages,entries=getPages(request,entries)  #将Paginator封装成函数了

    context={'topic':topic,'entries':entries,'pages':pages}
    return render(request,'blog/topic.html',context)

# @login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':
        #未提交数据：创建一个新表单
        form = TopicForm()
    else:
        #POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            # form.save()
            return HttpResponseRedirect(reverse('blog:topics'))

    context={'form':form}
    return render(request,'blog/new_topic.html',context)

# @login_required
def new_entry(request,topic_id):
    '''在特定的主题中添加新条目'''
    topic=Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #未提交数据，创建一个空表单
        form=EntryForm()
    else:
        #POST提交的数据，对数据进行处理
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('blog:topic',args=[topic_id]))

    context={'topic':topic,'form':form}
    return render(request,'blog/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    '''编辑既有条目'''
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic

    if topic.owner !=request.user:
        # raise Http404
        return render(request,'blog/404_edit.html')

    if request.method != 'POST':
        #初次请求，使用当前条目填充表单
        form=EntryForm(instance=entry)
    else:
        #POST提交的数据，对数据进行处理
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topic',args=[topic.id]))

    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'blog/edit_entry.html',context)

def detail_entry(request,entry_id):
    try:
        entry=Entry.objects.get(id=entry_id)
        topic=entry.topic
        entry.increase_read_num()
        # 获取前后各一篇博文,QuerySet的写法，毕竟SQL查询可读性不强,所以没有使用。
        #__gt和__lt分别是大于和小于的意思。可以修饰到判断条件的字段上
        pre_entry = Entry.objects.filter(id__gt=entry_id).order_by('id')
        next_entry = Entry.objects.filter(id__lt=entry_id).order_by('-id')

        #取第1条记录
        if pre_entry.count() > 0:
            pre_entry = pre_entry[0]
        else:
            pre_entry = None

        if next_entry.count() > 0:
            next_entry = next_entry[0]
        else:
            next_entry = None

        context={'topic':topic,'entry':entry,'pre_entry':pre_entry,'next_entry':next_entry}
    except Entry.DoesNotExist:
        raise Http404
    return render(request,'blog/detail_entry.html',context)

def search(request):
    """show blogs' list"""
    try:
        search_key=request.GET['search_key']
        if not search_key:
            return index(request)
        entries = Entry.objects.filter(title__contains=search_key)
        pages,entries=getPages(request,entries)  #将Paginator封装成函数了
        context={'entries':entries,'pages':pages,'search_key':search_key}
    except Exception:
        raise Http404
    return render_to_response('blog/blog_search.html',context)
    # return render(request,'blog/blog_search.html',context)

def getPages(request,list1,limit=7): # limit 每页显示的记录数
    # 未优化前
    # pages = Paginator(list1, limit)  # 实例化一个分页对象
    # page = request.GET.get('page',1)  # 获取GET请求的参数，得到当前页码。若没有该参数，默认为1
    # try:
    #     list1 = pages.page(page)  # 获取某页对应的记录
    # except PageNotAnInteger:  # 如果页码不是个整数
    #     list1 = pages.page(1)  # 取第一页的记录
    # except EmptyPage:  # 如果页码太大，没有相应的记录
    #     list1 = pages.page(pages.num_pages)  # 取最后一页的记录
    # return pages,list1

    # 优化后
    currentPage = request.GET.get('page', 1)
    paginator = Paginator(list1,limit)
    try:
        list1 = paginator.page(currentPage)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        list1 = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        list1 = paginator.page(paginator.num_pages)  # 取最后一页的记录
    page_range = []
    current = list1.number     #当前页码
    page_all = paginator.num_pages  #总页数
    mid_pages = 3                   #中间段显示的页码数
    page_goto = 1                    #默认跳转的页码

    #获取优化显示的页码列表
    if page_all <= 5+ mid_pages:
        #页码数少于6页就无需分析哪些地方需要隐藏
        page_range = paginator.page_range
    else:
        #添加应该显示的页码
        page_range += [1, page_all]
        page_range += [current-2, current, current+2]

        #若当前页是头尾，范围拓展多1页
        if current == 1 or current == page_all:
            page_range += [current+2, current-2]

        #去掉超出范围的页码
        page_range = filter(lambda x: x>=1 and x<=page_all, page_range)

        #排序去重
        #此处list踩坑，原先list与形参list则会到会使list()优先形参解释，导致错误
        page_range = sorted(list(set(page_range)))

        #查漏补缺
        #从第2个开始遍历，查看页码间隔，若间隔为0则是连续的
        #若间隔为1则补上页码；间隔超过1，则补上省略号
        t = 1
        for i in range(len(page_range)-1):
            step = page_range[t]-page_range[t-1]
            if step>=2:
                if step==2:
                    page_range.insert(t,page_range[t]-1)
                else:
                    page_goto = page_range[t-1] + 1
                    page_range.insert(t,'...')
                t+=1
            t+=1

    #优化结果之后的页码列表
    paginator.page_range_ex = page_range
    #默认跳转页的值
    paginator.page_goto = page_goto

    return paginator,list1