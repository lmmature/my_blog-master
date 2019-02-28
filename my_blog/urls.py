"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
# from django.contrib import admin
from show import views as show_views
from backstage import views as backstage_views
import debug_toolbar
import django_cas_ng.views

# backstage
urlpatterns = [
    url(r'^debug', include(debug_toolbar.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'upload/', backstage_views.upload, name='upload'),
    url(r'quit', backstage_views.out),
    url(r'manage/page/(\d+)', backstage_views.edit, name='edit_paper'),
    url(r'manage', backstage_views.manage, name="manage_paper"),
    url(r'hide', backstage_views.manage_hide, name="manage_paper_hide"),
    url(r'add/text', backstage_views.add_text, name="add_paper_text"),
    url(r'add/markdown', backstage_views.add_markdown, name="add_paper_markdown"),
    url(r'article_sum', backstage_views.article_sum),
    url(r'^admin/', backstage_views.index, name='manage_index'),

]
# show
urlpatterns += [
    url(r'^$', show_views.index, name="show_index"),
    url(r'blog/(\w*-?\w*)?$', show_views.blog, name="blogs"),
    url(r'contact', show_views.contact, name="contact"),
    url(r'about', show_views.about, name="about"),
    url(r'single/paper/(\d+)', show_views.single, name='single_paper_show'),
]
# cas
urlpatterns += [
    url(r'^accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),  # 认证跳转
    url(r'^accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),  # 注销
]
