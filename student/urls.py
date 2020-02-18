from django.urls import re_path
from student import views


urlpatterns = [
    # re_path(r'^$', views.dashboard, name='sales_dashboard'),
    re_path(r'^my_courses/$', views.my_courses),


]