# _*_ coding:utf-8 _*_
__author__ = 'luqi'
__date__ = ' 14:46'


from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, AddFavView, CourseInfoView
urlpatterns=[
    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    #收藏
    url(r'^add_fav/$',  AddFavView.as_view(),name='add_fav'),
    #课程视频信息页
    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info')


 ]

                                               