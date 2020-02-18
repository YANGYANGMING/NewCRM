from django.template import Library
from django.utils.safestring import mark_safe
import time, datetime


register = Library()

@register.simple_tag
def bulid_filter_ele(filter_column, admin_class):
    """生成筛选字段的html ele"""
    filter_ele = "<div class='col-md-2'>%s<select class='form-control' name=%s>" % (filter_column, filter_column)
    column_obj = admin_class.model._meta.get_field(filter_column)
    print('column_obj', column_obj)
    try:
        for choice in column_obj.get_choices():
            selected = ''
            """column_obj.get_choices() = [('', '---------'), (0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其它')]"""
            if filter_column in admin_class.filter_conditions:#当前字段被过滤了
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):#当前值被选中
                    selected = 'selected'
            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:
        print('err', e)
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            filter_ele = "<div class='col-md-2'>%s<select class='form-control' name=%s__gte>" % (filter_column, filter_column)
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月内'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay'],
            ]
            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % filter_column in admin_class.filter_conditions:  # 当前字段被过滤了
                    if time_to_str == admin_class.filter_conditions.get("%s__gte" % filter_column):#当前值被选中
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % (time_to_str, selected, i[1])
                filter_ele += option

    filter_ele += '</select></div>'

    return mark_safe(filter_ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def bulid_table_row(obj, admin_class):
    """生成一条表td的html element"""
    ele = ''
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:  #表示有choices, 即可以get_xxx_display
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_data = getattr(obj, column_name)
            tb_ele = "<td>%s</td>" % column_data
            if index == 0:
                tb_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, column_data)
            ele += tb_ele
    else:
        tb_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)
        ele += tb_ele
    return mark_safe(ele)  #返回一行数据

@register.simple_tag
def get_sorted_column(sorted_column, forloop, column):
    """判断上次排序方式，并取反"""
    #sorted_column = {'name': '-0'}
    if column in sorted_column:  #这一列被排序
        #判断上一次排序是什么顺序，本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = "-%s" % last_sort_index
        return this_time_sort_index
    else:
        return forloop

@register.simple_tag
def render_filtered_args(admin_class, render_html=True):
    """BUG1解决：点击排序时，在排序url后拼接筛选url, render_html用来解决点击分页，筛选消失的问题"""
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += "&%s=%s" % (k, v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''


@register.simple_tag
def render_sorted_arrow(column, sorted_column):
    """生成排序的上下箭头html ele"""
    if column in sorted_column:  # 这一列被排序
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = """<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>""" % arrow_direction
        return mark_safe(ele)
    return ''

@register.simple_tag
def renber_panginator(querysets, admin_class, sorted_column):
    """生成分页的html ele"""
    ele = """
        <ul class="pagination">
        """
    get_filter_ele = render_filtered_args(admin_class) #解决点击分页，筛选消失的问题
    sorted_ele = ''
    if sorted_column: #解决点击分页，排序消失的问题
        sorted_ele += "&_o=%s" % list(sorted_column.values())[0]

    if querysets.has_previous():
        first_ele = """<li><a href="?_page=1%s%s">首页</a></li>""" % (get_filter_ele, sorted_ele)
        p_ele = """<li><a href="?_page=%s%s%s">上一页</a></li>""" % (querysets.previous_page_number(), get_filter_ele, sorted_ele)
    else:
        first_ele = """<li><a href="?_page=1%s%s">首页</a></li>""" % (get_filter_ele, sorted_ele)
        p_ele = """<li><a href="?_page=1%s%s">上一页</a></li>""" % (get_filter_ele, sorted_ele)
    ele += first_ele + p_ele
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < 2:
            active = ''
            if querysets.number == i:
                active = 'active'
            p_ele = """<li class="%s"><a href="?_page=%s%s%s">%s</a></li>""" % (active, i, get_filter_ele, sorted_ele, i)
            ele += p_ele
    if querysets.has_next():
        p_ele = """<li><a href="?_page=%s%s%s">下一页</a></li>""" % (querysets.next_page_number(), get_filter_ele, sorted_ele)
        last_ele = """<li><a href="?_page=%s%s%s">尾页</a></li>""" % (querysets.paginator.num_pages, get_filter_ele, sorted_ele)
    else:
        p_ele = """<li><a href="?_page=%s%s%s">下一页</a></li>""" % (querysets.paginator.num_pages, get_filter_ele, sorted_ele)
        last_ele = """<li><a href="?_page=%s%s%s">尾页</a></li>""" % (querysets.paginator.num_pages, get_filter_ele, sorted_ele)
    ele += p_ele + last_ele
    ele += "</ul>"
    return mark_safe(ele)

@register.simple_tag
def get_current_sorted_column_index(sorted_column):

    return list(sorted_column.values())[0] if sorted_column else ''


@register.simple_tag
def get_obj_field_value(form_obj, field):
    """返回modelobj具体字段的值"""
    return getattr(form_obj.instance, field)

@register.simple_tag
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
    """返回的是m2m字段关联表的所有数据"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())
        return obj_list - selected_data  #排除有边框已有的数据
    else:
        return obj_list

@register.simple_tag
def get_selected_m2m_data(field_name, form_obj, admin_class):
    """返回已选的m2m字段"""
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance, field_name).all()
        return selected_data
    else:
        return []

@register.simple_tag
def display_all_related_objs(obj):
    """显示要被删除对象的所有对象
    :param obj
    :return:
    """
    ele = "<ul><b style='color:red'>%s</b>" % obj
    # ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" % (obj._meta.app_label, obj._meta.model_name, obj.id, obj)

    for received_fk_obj in obj._meta.related_objects:
        related_table_name = received_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()
        ele += "<li>%s<ul>" % related_table_name

        if received_fk_obj.get_internal_type() == "ManyToManyField": #不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a>  记录里与[%s]相关的数据将被删除</li>" % \
                       (i._meta.app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                # ele += "<li>%s123</li>" % i
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" % \
                (i._meta.app_label, i._meta.model_name, i.id, i)

                ele += display_all_related_objs(i)
        ele += "</ul></li>"
    ele += "</ul>"
    return ele




























