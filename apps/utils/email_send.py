#coding=utf-8
__author__ = 'luqi'
__date__ = ' 15:24'

from random import Random


from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM
#发送邮箱注册验证码
def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16) #随机字符串，即EmailVerfyRecord()中的code字段
    email_record.code = code
    email_record.email =email
    email_record.send_type=send_type
    email_record.save()

    if send_type=='register':
        email_title ='慕学网注册链接激活'
        email_body =u'请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])  #  提前设置setting后可直接给send_mail()使用,先要调用settings
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '慕学网密码重置'
        email_body = u'请点击下面链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


#s生成随机字符串函数
def generate_random_str(randomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random = Random()
    for i in  range(randomlength):
        str+=chars[random.randint(0,length)]
    return str
