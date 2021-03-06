"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from users import views

urlpatterns = [
    url(r"^mobile_code/$", views.SendMobileCodeView.as_view()),  # 发送短信验证码
    url(r"^user_name/$", views.ValidateNameView.as_view()),  # 验证用户名
    url(r'^register/$', views.RegisterView.as_view()),  # 注册
    url(r'^login/$', views.LoginView.as_view()),  # 登录

    url(r'^address/$', views.AddressView.as_view()),  # 用户中心地址
    url(r'^address/(?P<pk>\d+)$', views.DelAddressView.as_view()),  # 删除地址
    url(r'^def_address/$', views.DefAddressView.as_view()),  # 设置默认地址
]

