#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser   #系统提供的auth_user表，我们创建的model要继承之
# Create your models here.



#用户属性表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default="")
    birday=models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(choices=(("male","男"),('female',"女")),default="female",max_length=10)
    address = models.CharField(max_length=100,default=u"")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)#max_length,image在后台以字符串存储

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.username #继承自AbstractUser的属性
#邮箱验证码信息表
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email=models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register',u'注册'),('forget',u'找回密码')),max_length=10,verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')  ### 不能写成now(),那样在类创建的时候就记录时间了，我们要等到实例化类才能记录时刻

    class Meta:
        verbose_name=u'邮箱验证码'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)

#轮播图信息表
class Banner(models.Model):
    title =models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图',max_length=100)
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index=models.IntegerField(default=100,verbose_name=u'顺序')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name='轮播图'
        verbose_name_plural=verbose_name
