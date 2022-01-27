

## 运行环境
在python3.7,Django2.2版本下测试运行成功，windows,linux平台。
## 运行步骤
首先安装好运行环境，配置好python虚拟环境，可以不使用虚拟环境,进入LmsWeb目录
```bash
#安装requirements.txt依赖包（环境）
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
#上面两步进行迁移，完成数据库表的建立

python manage.py runserver
#默认端口开在127.0.0.1:8000

#创建超级管理员用户
python manage.py createsuperuser

```
然后浏览器打开127.0.0.1:8000/进入管理系统


#页面展示

##首页






