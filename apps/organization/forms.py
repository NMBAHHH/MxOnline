#_*_ encoding=utf-8 _*_
__author__ = 'luqi'
__date__ = ' 13:40'

from django import forms

from operation.models import UserAsk

import re #正则表达式
#
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone=forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=5)


#   使用ModelFrom来改写UserForm
#   相比Form，ModelForm功能更强大，可以继承已有modle，也可以直接save()，像modle一样
class UserAskForm(forms.ModelForm):
    #xxx=forms.CharField(。。。) 除了继承，还能扩写

    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']

    #   验证手机号码是否合法
    def clean_mobile(self):
        #   对mobile字段做判断（譬如必须是11位手机号格式），注意这个函数是固定名称的，必须是  "mobile+字段名" 格式
        #   并且在初始化form的时候会自动调用此函数
        #   实际上clean_xxx函数可以看成对ModelForm类型变量的自定义再封装

        mobile = self.cleaned_data['mobile'] #取出mobile数据
        #  正则表达式判断手机号
        REGEX_MOBILE= "1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise  forms.ValidationError(u'手机号码非法',code='mobile_invailable ')




                                               