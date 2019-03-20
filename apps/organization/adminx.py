#_*_ conding:utf-8 _*_
__author__ = 'luqi'
__date__ = ' 17:07'



import xadmin

from .models import CityDict,CourseOrg,Teacher


class CityDict_ogz(object):
    list_display = ['name', 'add_time','desc']
    search_fields = ['name','desc']
    list_filter = ['name', 'add_time','desc']


class CourseOrg_ogz(object):
    list_display = ['name', 'desc', 'click_nums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_nums','image','address','city']
    list_filter = ['name', 'desc', 'click_nums','image','address','city','add_time']


class Teacher_ogz(object):
    list_display = ['org','name','work_years','work_company','work_position','points','click_nums','fav_num','add_time']
    search_fields = ['org','name','work_years','work_company','work_position','points','click_nums','fav_num']
    list_filter = ['org','name','work_years','work_company','work_position','points','click_nums','fav_num','add_time']


xadmin.site.register(CityDict,CityDict_ogz)
xadmin.site.register(CourseOrg,CourseOrg_ogz)
xadmin.site.register(Teacher,Teacher_ogz)