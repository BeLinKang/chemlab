import datetime
import json

from dateutil.relativedelta import relativedelta
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
# Create your views here.
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import UserCustomRegister, UserCustomChange
from django.contrib.auth.models import User


def index(request):
    if request.method == 'GET':
        MedicineList = Medicine.objects.all()
        LabList = Lab.objects.all()
        # 将数据按照规定每页显示 8 条, 进行分割
        paginator = Paginator(MedicineList, 8)

        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        medicineList = paginator.get_page(page)

        # try:
        #     medicineList = paginator.page(page)
        # # todo: 注意捕获异常
        # except PageNotAnInteger:
        #     # 如果请求的页数不是整数, 返回第一页。
        #     medicineList = paginator.page(1)
        # except EmptyPage:
        #     # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        #     medicineList = paginator.page(paginator.num_pages)
        # except InvalidPage:
        #     # 如果请求的页数不存在, 重定向页面
        #     return HttpResponse('找不到页面的内容')

        content = {
            'medicineList': medicineList,
            'LabList': LabList,
            'currentUser': request.user,
        }

        return render(request, 'lms/index.html', content)


def lab(request):
    LabList = Lab.objects.all()

    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(LabList, 10)

    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')

    try:
        labList = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        labList = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        labList = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    content = {
        'labList': labList,

    }
    return render(request, 'lms/lab.html', content)


def about(request):
    # need id to define special book
    return render(request, 'lms/about.html')


def medicineSearch(request):
    """
    注意这里的 MedicineList 与分页 medicineList不能同名

    """
    LabList = Lab.objects.all()

    if request.method == 'POST':
        searchType = request.POST['searchType']
        keyword = request.POST['keyword']
        # print(searchType, keyword)
        if searchType == 'name':
            MedicineList = Medicine.objects.filter(name__contains=keyword)
            # print("ky1:" + str(medicineList))

        elif searchType == 'number':
            MedicineList = Medicine.objects.filter(number__contains=keyword)
            # print("ky2：" + str(medicineList))

        else:
            # print("xixxixiix")
            MedicineList = Medicine.objects.filter(Q(name__contains=keyword) |
                                                   Q(number__contains=keyword))
            # print("ky3:" + str(medicineList))

        # 将数据按照规定每页显示 8 条, 进行分割
        paginator = Paginator(MedicineList, 8)

        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')

        medicineList = paginator.get_page(page)
        # try:
        #     # medicineList = paginator.page(page)
        #     medicineList = paginator.get_page(page)
        # # todo: 注意捕获异常
        # except PageNotAnInteger:
        #     # 如果请求的页数不是整数, 返回第一页。
        #     medicineList = paginator.get_page(1)
        # except EmptyPage:
        #     # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        #     medicineList = paginator.get_page(paginator.num_pages)
        # except InvalidPage:
        #     # 如果请求的页数不存在, 重定向页面
        #     return HttpResponse('找不到页面的内容')

        content = {'medicineList': medicineList,
                   'LabList': LabList,
                   'currentUser': request.user
                   }
        return render(request, 'lms/index.html', content)


# 登陆注册

def loging(request):
    # 登录模块
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'lms/login.html', {'error': '用户名不存在或密码错误'})
        else:
            login(request, user)
            return redirect('lms:lms_index')
    else:
        return render(request, 'lms/login.html')


# 登出
def logouting(request):
    logout(request)
    return redirect('lms:lms_index')


# 注册
def register(request):
    if request.method == 'POST':
        registerForm = UserCustomRegister(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            newUser = authenticate(username=registerForm.cleaned_data['username'],
                                   password=registerForm.cleaned_data['password1'])
            newUser.email = registerForm.cleaned_data['email']
            CommonUser(user=newUser, nickyName=registerForm.cleaned_data['nickyName'],
                       cate=registerForm.cleaned_data['cate'],
                       faculty=registerForm.cleaned_data['faculty']).save()
            login(request, newUser)
            return redirect('lms:lms_index')
    else:

        registerForm = UserCustomRegister()
    content = {'registerForm': registerForm}
    return render(request, 'lms/register.html', content)


# 学生信息
@login_required(login_url='lms:login')
def userCentre(request):
    # need id to define special user
    if request.method == 'POST':
        changeForm = UserCustomChange(request.POST, instance=request.user)
        if changeForm.is_valid():
            changeForm.save()
            request.user.commonuser.nickyName = changeForm.cleaned_data['nickyName']
            request.user.commonuser.save()
            # 关联的表要另外存储
            # newUser.email = registerForm.cleaned_data['email']
            # CommonUser(user=newUser, nickyName=registerForm.cleaned_data['nickyName'],
            #            cate=registerForm.cleaned_data['cate'],
            #            faculty=registerForm.cleaned_data['faculty']).save()
    else:
        pass
    changeForm = UserCustomChange()
    content = {'currentUser': request.user, 'changeForm': changeForm}
    return render(request, 'lms/userCentre.html', content)


# 学生修改密码
@login_required(login_url='lms:login')
def changePassword(request):
    if request.method == 'POST':
        changepasswordForm = PasswordChangeForm(data=request.POST, user=request.user)
        if changepasswordForm.is_valid():
            changepasswordForm.save()
            return redirect('lms:login')
    else:
        pass
    changepasswordForm = PasswordChangeForm(user=request.user)
    content = {
        'currentUser': request.user,
        'changepasswordForm': changepasswordForm
    }
    return render(request, 'lms/changePassword.html', content)


# 学生借阅历史查看
@login_required(login_url='lms:login')
def borrowHistory(request):
    # need id to define special user
    if request.method == 'GET':
        user = CommonUser.objects.filter(user=request.user).first()
        MedicineListTarget = Borrow.objects.filter(user=user).order_by("-boDate")
        MedicineList = []
        for borrowInfo in MedicineListTarget:
            borrowTime = datetime.datetime.now().day - borrowInfo.boDate.day
            MedicineList.append((Medicine.objects.get(pk=borrowInfo.medicine_id), borrowInfo, borrowTime))

        # chart_info = Borrow.objects.filter(user=user).values_list('medicine').annotate(Count('id'))
        # print(chart_info)

        content = {
            'MedicineList': MedicineList,
            'currentUser': request.user
        }
        return render(request, 'lms/borrowHistory.html', content)


# 药品详情表
def medicineDetail(request, medicineId):
    if request.method == 'GET':
        thisMedicine = Medicine.objects.get(id=medicineId)
        content = {
            'medicine': thisMedicine,
        }
        return render(request, 'lms/detail.html', content)


#
@login_required(login_url='lms:login')
def subAndBo(request, medicine_id):
    LabList = Lab.objects.all()
    if request.method == 'POST':

        thisLab = request.POST.get('lab')
        print(thisLab)
        thisNum = int(request.POST.get('medicineUsedNum'))
        thisUser = User.objects.get(pk=request.user.id)
        # p判断实验室是否存在
        labTrue = Lab.objects.filter(name__exact=thisLab).count()
        print(labTrue)
        # if (thisLab == ''):
        #     thisLab = "ooo"
        #     得到了的Lab为空值？
        # print(thisLab, thisNum, thisUser)
        thisMedicine = Medicine.objects.get(pk=medicine_id)
        # print(medicine_id)
        if thisMedicine.nowtotal <= thisNum:
            # return HttpResponse("失败！库存不足！")
            # return JsonResponse({"failInfo": "失败！库存不足！"})
            return render(request, 'lms/error.html', {"failInfo": "失败！库存不足！"})


        elif labTrue == 0:
            return render(request, 'lms/error.html', {"failInfo": "请输入正确的实验室名称"})

            # return HttpResponse("请输入正确的实验室名称")

        else:
            thisMedicine.usedtotal += thisNum
            thisMedicine.nowtotal -= thisNum
            thisMedicine.save()
            newBorrow = Borrow(user=thisUser.commonuser, lab=Lab.objects.get(name=thisLab),
                               medicine=thisMedicine, medicineUsedNum=thisNum)
            newBorrow.save()

            # content = {
            #     'MedicineList': Medicine.objects.all(),
            #     'LabList': Lab.objects.all(),
            #     'currentUser': request.user,
            #     'successInfo': '成功',
            #
            # }
            # return HttpResponse('你好' + str(thisNum) + " :" + str(thisLab) + "->" + str(thisUser))
            # return render(request, 'lms/index.html', content)

            return redirect('lms:lms_index')
    # else:
    #     content = {
    #         'MedicineList': Medicine.objects.all(),
    #         'LabList': Lab.objects.all(),
    #         'currentUser': request.user,
    #         'failInfo': '失败',
    #
    #     }
    # return render(request, 'lms/index.html', content)


def chart1(request):
    chartMedicine = Medicine.objects.all()[0:15]
    name_list = []  # 设置为list类型，一会儿将其填入data中
    used_list = []  # 设置为list类型，一会儿将其填入data中
    now_list = []  # 设置为list类型，一会儿将其填入data中

    for medicine in chartMedicine:
        name_list.append(medicine.name)
        used_list.append(medicine.usedtotal)
        now_list.append(medicine.nowtotal)
    # print(name_list)
    # print(now_list)
    # print(used_list)

    # 每天计数
    chartBorrow = Borrow.objects.extra({'boDate': "date(boDate)"}).values_list('boDate').annotate(count=Count('id'))
    # print(chartBorrow)
    # <QuerySet [(datetime.date(2021, 9, 25), 2), (datetime.date(2021, 9, 27), 1), (datetime.date(2021, 9, 30), 1)]>
    bo_list = []
    count_list = []
    for bo in chartBorrow:
        bo_list.append(bo[0].strftime('%Y-%m-%d'))
        count_list.append(bo[1])

    # print(bo_list)
    # print(count_list)
    # [datetime.date(2021, 9, 25), datetime.date(2021, 9, 27), datetime.date(2021, 9, 30)]
    # [2, 1, 1]

    content = {
        # 1
        'name_list': name_list,
        'used_list': used_list,
        'now_list': now_list,
        # 2
        'bo_list': bo_list,
        'count_list': count_list

    }

    return render(request, 'lms/chart1.html', content)


def chart2(request):
    """查询近一周借用数量最多的药品的数量前五"""
    today = datetime.datetime.now()
    lastweek = (datetime.datetime.now() - relativedelta(months=1))
    # print(today)

    cursor = connection.cursor()
    sql1 = "select sum(medicineUsedNum) totalUsed, medicine_id, name " \
           "from lms_borrow,lms_medicine where lms_borrow.medicine_id=lms_medicine.id and boDate between %s and %s group by medicine_id order by totalUsed limit 5"

    cursor.execute(sql1, [lastweek, today])
    ret1 = cursor.fetchall()
    # print(ret)
    # ((Decimal('10'), 21, '二甲基甲苯'), (Decimal('12'), 11, '氯化钠'))
    name_list = []
    used_list = []
    for i in ret1:
        name_list.append(i[2])
        used_list.append(int(i[0]))

    #
    cursor = connection.cursor()
    sql2 = "select  nickyName,count(*) record " \
           "from lms_borrow,lms_commonuser where lms_borrow.user_id = lms_commonuser.id " \
           "and boDate between %s and %s " \
           "group by lms_borrow.user_id order by record limit 5"

    cursor.execute(sql2, [lastweek, today])
    ret2 = cursor.fetchall()
    print(ret2)

    user_list = []
    count_list = []
    for i in ret2:
        user_list.append(i[0])
        count_list.append(i[1])

    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(user_list, count_list):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端

    # rep = []
    #
    # for i in list(ret2):
    #     tem = {"value": i[1], "name":i[0]}
    #     rep.append(tem)
    #
    # print(rep)
    context = {
        'name_list': name_list,
        'used_list': used_list,
        # 'user_list': user_list,
        # 'count_list': count_list
        'data': json.dumps(data),
        # 'rep':rep
    }
    print(context)

    return render(request, 'lms/chart2.html', context)


# 总的登录界面
def loginOfAll(request):
    return render(request, 'lms/loginOfAll.html')
