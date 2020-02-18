from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from kingadmin import app_setup
from kingadmin.sites import site
from kingadmin import form_handle
from kingadmin import permissions
from crm import models
import json

app_setup.kingadmin_auto_discover()

print('site', site.enabled_admins)

def app_index(request):
    return render(request, 'kingadmin/app_index.html', {'site': site})

def get_filter_result(request, querysets):
    filter_conditions = {}
    for key, val in request.GET.items():
        if key in ("_page", "_o", "_q"):
            continue
        if val:
            filter_conditions[key] = val
    # print('filter_conditions', filter_conditions)
    return querysets.filter(**filter_conditions), filter_conditions

def get_orderby_result(request, querysets, admin_class):
    """排序"""
    current_ordered_column = {}
    orderby_index = request.GET.get("_o")
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_ordered_column[orderby_key] = orderby_index  #让前端知道当前排序的列

        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key

        return querysets.order_by(orderby_key), current_ordered_column
    else:
        return querysets, current_ordered_column

def get_search_result(request, querysets, admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = "OR"
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_key))
        return querysets.filter(q)
    else:
        return querysets


@permissions.check_permission
@login_required
def table_obj_list(request, app_name, model_name):
    """取出指定model里的数据返回给前端"""
    # print("app_name, model_name:", site.enabled_admins[app_name][model_name])
    admin_class = site.enabled_admins[app_name][model_name]

    if request.method == "POST":
        print(request.POST)
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids') )
        print(selected_action,selected_ids)
        if not selected_action: # 如果有action参数,代表这是一个正常的action,如果没有,代表可能是一个删除动作
            if selected_ids:#这些选中的数据都要被删除
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else: #走action流程
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class,selected_action)
            response = admin_action_func(request,selected_objs)
            if response:
                return response

    querysets = admin_class.model.objects.all().order_by("-id")  # model_class object

    # filter queryset result
    querysets, filter_conditions = get_filter_result(request, querysets)
    admin_class.filter_conditions = filter_conditions
    print(filter_conditions)
    print(request.GET)

    #searched queryset result
    querysets = get_search_result(request, querysets, admin_class)
    admin_class.search_key = request.GET.get("_q", "") #搜索后仍显示上次搜索内容

    #sorted_querysets result
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    #对过滤后的数据分页
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
    page = request.GET.get('_page')
    try:
        querysets = paginator.get_page(page)
    except PageNotAnInteger:
        querysets = paginator.get_page(1)
    except EmptyPage:
        querysets = paginator.get_page(paginator.num_pages)

    return render(request, 'kingadmin/table_obj_list.html', locals())


@permissions.check_permission
@login_required
def table_obj_change(request, app_name, model_name, obj_id):
    """kingadmin 数据修改页"""
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    print(model_form)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "GET":
        form_obj = model_form(instance=obj) #instance当前正在修改的对象
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()  #ModelForm直接保存，Form需要从clean_data中取出数据
            return redirect('/kingadmin/%s/%s/' % (app_name, model_name))

    return render(request, "kingadmin/table_obj_change.html", locals())


@permissions.check_permission
@login_required
def table_obj_add(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class, form_add=True)

    if request.method == "GET":
        form_obj = model_form()
    elif request.method == "POST":
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s/' % (app_name, model_name))

    return render(request, "kingadmin/table_obj_add.html", locals())


@permissions.check_permission
@login_required
def table_obj_delete(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)

    if request.method == "POST":
        obj.delete()
        return redirect("/kingadmin/%s/%s/" % (app_name, model_name))

    return render(request, "kingadmin/table_obj_delete.html", locals())

def acc_login(request):
    """登录"""
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            print("passed authentication")
            login(request, user)  #把user封装到request.session中
            return redirect(request.GET.get('next', '/kingadmin/'))  #登录后跳转至next指定的页面，否则到首页/
        else:
            error_msg = "Wrong username or password!"

    return render(request, 'kingadmin/login.html', locals())

def acc_logout(request):
    """退出"""
    # request.session.clear()
    logout(request)
    return redirect('/login/')









