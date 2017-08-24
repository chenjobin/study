from django.shortcuts import render_to_response,render
from .models import SubjectType, SubjectStaticType, Subject, SubjectChapter, SubjectItem

from django.http import Http404
from django.core.urlresolvers import reverse #url逆向解析
from django.template import RequestContext
# from apps_project.view_record.decorator import record_view #阅读计数

def index(request):
    # subjects = Subject.objects.all()
    subjects = Subject.objects.order_by('-create_time')
    data = {}
    data['subjects'] = subjects
    return render(request,'subject/index.html', data)

# @record_view(Subject)
def subject_show(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        chapters = []
        subject.increase_read_num()
        #数据统计
        blog_num = 0
        tutorial_num = 0

        #遍历章节
        for i, chapter in enumerate(subject.subjectchapter_set.all()):
            #遍历子项
            items = []
            for item in chapter.subjectitem_set.all():
                obj = item.content_type.get_object_for_this_type(id=item.object_id)
                obj_type = item.content_type.model

                #根据类型不同，设置名称和链接（动态绑定属性）
                if obj_type == 'entry':
                    item.type_name = '博客'
                    item.url = reverse('blog:detail_entry', args = [item.object_id,])
                    item.title = obj.title
                    blog_num += 1
                elif obj_type == 'tutorial':
                    item.type_name = '教程'
                    item.url = reverse('tutorial_detail', args = [item.object_id,])
                    item.title = obj.title
                    tutorial_num += 1
                else:
                    item.type_name = '未知'
                    item.url = '/'
                    item.title = '<未知的类型>'
                items.append(item)

            chapter.items = items
            chapter.sort_num = i + 1
            chapters.append(chapter)

    except Subject.DoesNotExist:
        raise Http404

    data = {}
    data['subject'] = subject
    data['chapters'] = chapters
    data['count'] = u'该专题分%s章节，共%s篇博客、%s个教程' % (len(chapters), blog_num, tutorial_num)
    # return render_to_response('subject/subject_show.html', data, context_instance=RequestContext(request))
    return render(request,'subject/subject_show.html', data)