# _*_ coding: utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from .models import  Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from operation.models import  UserFavorite
from django.http import HttpResponse



class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')  #默认最新排序


        #条件排序/筛选
        sort =request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')


        #对课程主页进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p  = Paginator(all_courses,6,request=request)
        cours = p.page(page)


        #热门课程推荐（right）
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]



        return render(request,'course-list.html',{
            'all_courses':cours , ##template中用xxx.object_list调用
            'sort': sort,
            'hot_courses':hot_courses ,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        #判断相关课程推荐
        tag = course.tag
        if tag:
           relate_courses=Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses= []

        #判断收藏与否
        is_fav_course = False
        is_fav_org = False
        if request.user.is_authenticated():
            user_fav_course = UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1)
            if user_fav_course:
                is_fav_course = True
        if request.user.is_authenticated():
            user_fav_org = UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2)
            if user_fav_org:
                is_fav_org = True

        return  render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'is_fav_course':is_fav_course,
            'is_fav_org':is_fav_org,
        })


#收藏按钮
class AddFavView(View):
    """
    用户收藏/取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        # 判断用户登陆状态
        if not request.user.is_authenticated():
            return  HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        else:
            exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
             #用户收藏记录已经存在（已登陆），则表示用户取消收藏
            if exist_records:
                exist_records.delete()
                return HttpResponse('{"status":"fail","msg":"取消收藏"}', content_type='application/json')

            else:
                if int(fav_type)>0 and int(fav_id>0):

                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class CourseInfoView(View):
     """
     课程章节信息
     """
     def get(self,request,course_id):
         course = Course.objects.get(id=int(course_id))
         course.
         return render(request, 'course-video.html', {
             'course': course,
         })
