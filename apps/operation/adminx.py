#_*_ conding:utf-8 _*_
__author__ = 'luqi'
__date__ = ' 16:06'

import  xadmin

from models import UserAsk,CourseComments,UserFavorite,Usermessage,UserCourse

class UserAsk_opera(object):
    list_display = ['name','mobile','course_name','add_time']
    search_fields = ['name','mobile','course_name']
    list_filter = ['name','mobile','course_name','add_time']


class CourseComments_opera(object):
    list_display = ['user','course','comment','add_time']
    search_fields = ['user','course','comment']
    list_filter = ['user','course','comment','add_time']


class UserFavorite_opera(object):
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter = ['user','fav_id','fav_type','add_time']


class Usermessage_opera(object):
    list_display = ['user', 'message', 'add_time','has_read']
    search_fields = ['user', 'message','has_read']
    list_filter = ['user', 'message', 'add_time','has_read']


class UserCourse_opera(object):
    list_display = ['user', 'course','add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course','add_time']

xadmin.site.register(UserAsk,UserAsk_opera)
xadmin.site.register(CourseComments,CourseComments_opera)
xadmin.site.register(UserFavorite,UserFavorite_opera)
xadmin.site.register(Usermessage,Usermessage_opera)
xadmin.site.register(UserCourse,UserCourse_opera)
