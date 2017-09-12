"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin


from DjangoUeditor import urls as DjangoUeditor_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include(DjangoUeditor_urls)),
    url(r'^users/',include('users.urls',namespace='users')),
    url(r'',include('blog.urls',namespace='blog')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'',include('subject.urls',namespace='subject')),
    url(r'',include('exam.urls',namespace='exam')),
]

# DjangoUeditor额外引入 ------use Django server /media/ files---------------------
from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 解决后台CSS丢失引入
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# DjangoUeditor额外引入 ----------------------------------------------------------