#_*_ coding:utf-8 _*_
from __future__ import unicode_literals

from django.apps import AppConfig


class OprationConfig(AppConfig):
    name = 'operation'
    #设定xadmin页面功能菜单的名称
    verbose_name=u'用户操作'