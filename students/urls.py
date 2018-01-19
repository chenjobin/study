from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$',
           views.StudentRegistrationView.as_view(),
           name='student_registration'),
    # 报名课程
    url(r'^enroll-course/$',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),

    url(r'^courses/$',views.StudentCourseListView.as_view(),name='student_course_list'),
    # 展示已报名课程
    url(r'^course/(?P<pk>\d+)/$',views.StudentCourseDetailView.as_view(),name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$',
        views.StudentCourseDetailView.as_view(),name='student_course_detail_module'),

]
