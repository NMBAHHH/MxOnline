# _*_ encoding:utf-8  _*_
__author__ = 'luqi'
__date__ = ' 16:44'



from django import forms
from captcha.fields import CaptchaField


#表单验证码captcha
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)    #变量名email必须与html中相关部件的name便签一致
    password = forms.CharField(required=True,min_length=5)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})


class LoginForms(forms.Form):
    username = forms.CharField(required=True,min_length=3) #     requireb是否必填,form 还有其他参数譬如max_length来限制表单数据格式
    password = forms.CharField(required=True,min_length=5)

#表单验证码captcha
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)    #变量名email必须与html中相关部件的name便签一致
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)  #名称和html中一致