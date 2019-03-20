#_*_ encoding=utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

import xadmin  #引入xadmin模块，将替代默认admin

from django.views.generic import  TemplateView
from django.views.static import serve #static多用于处理静态文件

from MxOnline.settings import MEDIA_ROOT

from users.views import LoginView , RegisterView ,ActiveUserView ,ForgetPwdView,ResetView,ModifyPwdView #自己定义的view login
from organization.views import OrgView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    #url(r'^login/$',user_login,name='login'，
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'register/$',RegisterView.as_view(),name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active'),  #正则，将active/之后所有字符串放在active_code中，P表示参数的意思
    url(r'^forget/$', ForgetPwdView.as_view(), name='forgrt_pwd'),
    url(r'reset/(?P<reset_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),


    #课程机构url配置，详情在oragnization/urls中,
    # #在html中org:org_list的org表示namespace，后面是name
    url(r'^org/',include('organization.urls',namespace='org')),

    #配置上传文件的访问处理函数（课程图片上传）
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),

    url(r'^course/',include('courses.urls',namespace='course')),

]


'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

'''
