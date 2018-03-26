"""aboutjuanli_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import (post_list, post_detail, post_year_archive, post_month_archive, tag_view, post_create, post_edit)


app_name = 'blog'
urlpatterns = [
   path('', post_list, name='post_list'),
   re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', post_detail,
           name='post_detail'),
   re_path(r'^(?P<year>\d{4})/$', post_year_archive, name='post_year_archive'),
   re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', post_month_archive, name="post_month_archive"),
   re_path(r'^tag/(?P<tag>[-\w]+)/$', tag_view, name='tag_view'),
   path('create/', post_create, name='post_create'),
   re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/edit/$', post_edit,
           name='post_edit'),
]

