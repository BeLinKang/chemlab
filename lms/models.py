from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Lab(models.Model):
    """实验室表"""

    class Meta:
        verbose_name = '实验室'
        verbose_name_plural = verbose_name

    name = models.CharField('实验室名', max_length=20)
    description = models.TextField('实验室描述', blank=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    """药品表"""

    class Meta:
        verbose_name = '药品列表'
        verbose_name_plural = verbose_name
        ordering = ('number',)

    # 药品信息类
    number = models.CharField('药品编号', max_length=13, unique=True)
    name = models.CharField('药品名', max_length=200)
    detail = models.TextField('药品信息', max_length=2000, blank=True)
    nowtotal = models.IntegerField('药品剩余量', default=0)
    usedtotal = models.IntegerField('药品用量', default=0)
    riskfactor = models.IntegerField('风险因子', default=0)

    def __str__(self):
        return self.name


class CommonUser(models.Model):
    """学生表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickyName = models.CharField('昵称', blank=True, max_length=50)
    cate = models.BooleanField('类别', default=False)
    # False stands for students, True represent Teacher
    faculty = models.CharField('系别', max_length=20, blank=True, default='undefine')

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)




class Borrow(models.Model):
    """借用药品纪录表"""

    class Meta:
        verbose_name = '借用记录'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(CommonUser, on_delete=models.CASCADE, verbose_name='借用人')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, verbose_name='借用地点')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='借用药品', )
    medicineUsedNum = models.PositiveIntegerField('药品使用量(/g)', default=0)
    boDate = models.DateTimeField('借用时间', auto_now_add=True)
