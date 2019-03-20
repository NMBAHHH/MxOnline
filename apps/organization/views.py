#_*_ encoding=utf-8 _*_m
from django.shortcuts import render
from django.views.generic import View

from .models import  CourseOrg,CityDict
from operation.models import  UserFavorite
# Create your views here.

#分页相关库
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from forms import  UserAskForm

from courses.models import Course

#用于返回json格式，项目组ajax使用
from django.http import  HttpResponse


class  OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]   # - 倒序排列

        #取出筛选城市
        city_id = request.GET.get('city','')  #得到一个string
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id)) ####此处第一个city_id 指的是数据库里的字段city，我们在model中定义了外键'city'，实际存储的时候，数据表中的字段名为'city_id'

        #s取出筛选的机构类型
        category = request.GET.get('ct', '')   #('pxjg','培训机构'),('gr','个人'),('gx','高校')
        if category:
            all_orgs = all_orgs.filter(category=category)


        #按照学习人数/课程数排列
        sort = request.GET.get('sort', '')
        if sort :
            if sort == 'students':
                all_orgs = all_orgs.order_by('-student')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        #————————————————————————————————————————————————-----------------------
        # 从get函数可以看到。org_nums显然如果太大了不好，需要分页
        # 分页参考https://github.com/jamespacileo/django-pure-pagination

        try:
            # 从前端获取当前页码数，默认为1(整型）
            page = request.GET.get('page ', 1)
            page =int(page)
        except PageNotAnInteger:
            # 如果用户输入的页码数不为整数
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        # 生成分页器对象，每页显示3条记录
        p = Paginator(all_orgs, 2,request=request)
        # 分页函数操，返回Page类实例，
        # #包含object_list, paginator,该page页的顶部和底部记录在object_lists中的位置，该页编号page
        orgs = p.page(page)
        #————————————————————————————————————————————————-----------------------
        return render(request,'org-list.html',{
            'all_orgs':orgs,  #template中用orgs.object_list调用
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #ModelForm不同与Model的地方是直接save到model中
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:

            #  切记！！！！！！json格式{}中为双引号！！！
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        # all_orgs = CourseOrg.objects.all()
        # hot_orgs = all_orgs.order_by('-click_nums')[:3]
        current_page='home'
        course_org = CourseOrg.objects.get(id =int(org_id))

        is_fav=False
        if request.user.is_authenticated():
            user_fav=UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                is_fav = True
        #   CourseOrg是course的外建，这样CourseOrg会给course一个函数去调用，即model名称小写_set,course_set()
        #   作用是反向的通过CourseOrg去获取course！！！！！
        all_courses = course_org.course_set.all()[:3]
        # teacher 中CourseOrg是外建，可以在CourseOrg中使用系统分配的teacher_set函数调用
        all_teacher = course_org.teacher_set.all()

        return  render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'is_fav':is_fav

        })



class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):

        current_page = 'course'
        course_org = CourseOrg.objects.get(id =int(org_id))

        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                is_fav = True
        #   CourseOrg是course的外建，这样CourseOrg会给course一个函数去调用，即model名称小写_set,course_set()
        #   作用是反向的通过CourseOrg去获取course！！！！！
        all_courses = course_org.course_set.all()
        # teacher 中CourseOrg是外建，可以在CourseOrg中使用系统分配的teacher_set函数调用
        # all_teacher = course_org.teacher_set.all()[:1]

        return  render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            # 'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'is_fav':is_fav
        })



class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):

        current_page = 'desc'
        course_org = CourseOrg.objects.get(id =int(org_id))

        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                is_fav = True
        #   CourseOrg是course的外建，这样CourseOrg会给course一个函数去调用，即model名称小写_set,course_set()
        #   作用是反向的通过CourseOrg去获取course！！！！！
        all_courses = course_org.course_set.all()
        # teacher 中CourseOrg是外建，可以在CourseOrg中使用系统分配的teacher_set函数调用
        # all_teacher = course_org.teacher_set.all()[:1]

        return  render(request,'org-detail-desc.html',{
            'all_courses':all_courses,
            # 'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'is_fav':is_fav
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self, request, org_id):

        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id =int(org_id))

        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                is_fav = True
        #   CourseOrg是course的外建，这样CourseOrg会给course一个函数去调用，即model名称小写_set,course_set()
        #   作用是反向的通过CourseOrg去获取course！！！！！
       # all_courses = course_org.course_set.all()
        #teacher 中CourseOrg是外建，可以在CourseOrg中使用系统分配的teacher_set函数调用
        all_teacher = course_org.teacher_set.all()

        return  render(request,'org-detail-teachers.html',{
            #'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'is_fav':is_fav
        })

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
                return HttpResponse('{"status":"fail","msg":"收藏"}', content_type='application/json')

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


