from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # 登录页
    path('', views.loginOfAll, name='loginOfAll'),
    # 学生端
    path('index', views.index, name='lms_index'),
    path('lab', views.lab, name='lab'),
    path('browseHistory', views.borrowHistory, name='borrowHistory'),
    path('userCentre', views.userCentre, name='userCentre'),
    path('changePassword', views.changePassword, name='changePassword'),
    path('about', views.about, name='about'),
    path('subAndBo/<int:medicine_id>', views.subAndBo, name='subAndBo'),
    path('login/', views.loging, name='login'),
    path('logout/', views.logouting, name='logout'),
    path('register/', views.register, name='register'),
    path('detail/<int:medicineId>', views.medicineDetail, name='medicineDetail'),
    path('medicineSearch/', views.medicineSearch, name='medicineSearch'),

    # admin中的
    path('admin/chart1/', views.chart1, name='chart1'),
    path('admin/chart2/', views.chart2, name='chart2'),
    path('admin/predict/', views.predict, name='predict'),
]
