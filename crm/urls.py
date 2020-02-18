from django.urls import re_path
from crm import views


urlpatterns = [
    re_path(r'^$', views.dashboard, name='sales_dashboard'),
    re_path(r'^stu_enrollment/$', views.stu_enrollment, name='stu_enrollment'),


]