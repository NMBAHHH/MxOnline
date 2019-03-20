#_*_ encoding=utf-8 _*_
__author__ = 'luqi'
__date__ = ' 09:58'

import xadmin

from .models import EmailVerifyRecord,Banner

#----------------
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView,BaseSetting)

class globalSettings(object):
     #xadmin的页眉
     site_title ='慕课后台管理系统'
     #xadmin页面页脚
     site_footer='慕学在线网'
     #xadmin导航菜单收缩
     menu_style ="accordion"


xadmin.site.register(views.CommAdminView ,globalSettings)
#----------------



class EmailVerifyfyRecordAdmin(object):    #将邮箱验证码功能放入xadmin
    list_display=['code','email','send_type','send_time']  #    列表页显示的字段
    search_fields =['code','email','send_type']   #在页面上增加搜索框，并确定可搜索的字段
    list_filter=['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title','image','url','send_time','add_time']
    search_fields = ['title','image','url','send_time']  # 在页面上增加搜索框，并确定可搜索的字段
    list_filter =  ['title','image','url','send_time','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyfyRecordAdmin) #xadmin 和 model关联注册
xadmin.site.register(Banner,BannerAdmin)