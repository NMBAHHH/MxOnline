#_*_ encoding=utf-8 _*_
__author__ = 'luqi'
__date__ = ' 14:36'



#将orgnization 有  关的urls配置单独放在organization的文件夹，防止MxOnline下面的urls太大太乱
#同时在MxOnline里的urls.py 需要用' include '字段标明此设置
from django.conf.urls import url, include

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns=[
    #课程机构首页
    url(r'^list/$',OrgView.as_view(),name='org_list'),

    #增加用户咨询表单
     url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),

    #
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(),name='org_home'),

    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(),name='org_course'),

    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(),name='org_desc'),

    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(),name='org_teacher'),

    #收藏
    url(r'^add_fav/$',  AddFavView.as_view(),name='add_fav')
 ]