from django.forms import ModelForm

def create_dynamic_model_form(admin_class, form_add=False):
    """动态生成 modelform
    form_add:False默认为修改表单， True时为添加表单
    """
    class Meta:
        model = admin_class.model  #类对象
        fields = "__all__"
        if not form_add: #修改
            exclude = admin_class.readonly_fields
            admin_class.form_add = False #这是因为自始至终admin_class实例都是同一个,
            # 这里修改属性为True是为了避免上一次添加调用将其改为了True
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:  #循环每一个字段
            field_obj = cls.base_fields[field_name]  #拿到每一个字段对象
            field_obj.widget.attrs.update({'class': 'form-control'})  # 给每个字段添加属性
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled': 'true'})  # 给每个字段添加属性

        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm", (ModelForm, ), {"Meta": Meta, '__new__': __new__})  #动态生成model模块

    print(dynamic_form)
    return dynamic_form








