from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry,Tag
from .forms import TopicForm,EntryForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.core.mail import send_mail #导入django发送邮件模块

# Create your views here.
def index(request):
    '''Blog的主页'''
    # return render(request,'blog/index.html') # 制作多个项目时，index,base等放templates根目录
    tags=Tag.objects.order_by('date_added')
    context={'tags':tags}
    return render(request,'blog/index.html',context)

def tag(request,tag_id):
    '''显示特定tag及其所有的条目'''
    limit = 7  # 每页显示的记录数
    tag=Tag.objects.get(id=tag_id)

    entries=tag.entry_set.order_by('-date_added')
    pages = Paginator(entries, limit)  # 实例化一个分页对象

    page = request.GET.get('page',1)  # 获取GET请求的参数，得到当前页码。若没有该参数，默认为1
    try:
        entries = pages.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        entries = pages.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        entries = pages.page(pages.num_pages)  # 取最后一页的记录

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

def getPages(request,list,limit=7): # limit 每页显示的记录数

    pages = Paginator(list, limit)  # 实例化一个分页对象
    page = request.GET.get('page',1)  # 获取GET请求的参数，得到当前页码。若没有该参数，默认为1
    try:
        list = pages.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        list = pages.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        list = pages.page(pages.num_pages)  # 取最后一页的记录

    return pages,list