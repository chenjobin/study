from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                         DeleteView
from .models import Course
# django1.9开始包含权限mixins给基于类的视图,所以和django BY example不同
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


# class OwnerCourseMixin(OwnerMixin):
#     model = Course
#
#
# class OwnerCourseEditMixin(OwnerMixin,OwnerEditMixin, LoginRequiredMixin):
#     model = Course
#     success_url = reverse_lazy('course:manage_course_list')
#     fields = ['subject', 'title', 'slug', 'overview']
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('course:manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('course:manage_course_list')
    permission_required = 'courses.delete_course'

