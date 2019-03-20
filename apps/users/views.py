# _*_ encoding:utf-8  _*_
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import  login ,authenticate
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import  Q

from django.views.generic.base import View
from .forms import LoginForms, RegisterForm,ForgetForm , ModifyPwdForm

from django.contrib.auth.hashers import make_password  # 密码加密
from utils.email_send import send_register_email

#ctrl+/批量注释
# def user_login(request):
#     if request.method=='POST':
#         username = request.POST.get('username','')
#         password =  request.POST.get('password','')
#         user = authenticate(username=username,password=password)    #函数判断usename/pw是否为真，否则返回None
#
#         if user is not None:
#             login(request,user)  #可以登陆（session和cokies）
#
#             return render(request, 'index.html', {})
#         else:
#             return render(request,'login.html',{'msg':"用户名密码错误！ "})
#     elif request.method == 'GET':
#         return render(request,"login.html",{})


#构造一个类来代替user_login等函数
class LoginView(View):
    def get(self,requset):
        return render(requset, "login.html", {})
    def post(self,request):
        #定义一个login_from类型的from对象
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)  # 函数判断usename/pw是否为真，否则返回None

            if user is not None:
                if user.is_active:    ###################################????????????????????????????????
                    login(request, user)  # 可以登陆（session和cokies）
                    return render(request, 'index.html',{})
                else:
                    return render(request, 'login.html', {'msg': "用户未激活！"})
            else:
                return render(request, 'login.html', {'msg': "用户名密码错误！"})
        else:
            return render(request, 'login.html', {'msg': "用户名密码错误！",'login_form':login_form})



class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return  render(request,'register.html',{'register_form':register_form} )
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name =request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'msg':'用户已存在！'})
            pass_word =request.POST.get('password')
            user_profile=UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active=False
            user_profile.password = make_password(pass_word)
            user_profile.save()   #将post上来的form里的数据保存到数据库

            #发送注册邮件
            send_register_email(user_name,'register')
            return render(request, 'login.html')


class ActiveUserView(View):
    def get(self,request,active_code):
        all_recode = EmailVerifyRecord.objects.filter(code=active_code)
        if all_recode:
            for record in all_recode:
                email =record.email
                user = UserProfile.objects.get(email=email)
                user.is_active =True
                user.save()
        else:
            return render(request,'active_fail.html')
        return  render(request,'login.html')



class ForgetPwdView(View):
    def get(self,request):
        forget_form =ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email,'forget')
            return  render(request,'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self,request,reset_code):
        all_recode = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_recode:
           for record in all_recode:
                email=record.email
                ###用户修改密码之后，需要把邮箱告诉后台，此处加入email，在前端加<input type=hidden value=email.....
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')

class ModifyPwdView(View):   #post的时候没有code参数在URL后面，所以不能和ResetView在一个class，新定义一个ModifyPwdView
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email','')
            if pwd2 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'两次输入的密码不一致！'})
            user=UserProfile.objects.get(email=email)
            user.password =make_password(pwd2)
            user.save()

            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form })









#可以自定义有关的表单的验证，通过重写authenticate，从可以通过邮箱验证（原来只能通过用户名验证）
class CustomBackend(ModelBackend):
    def authenticate(selfself,username=None,password=None,**kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



