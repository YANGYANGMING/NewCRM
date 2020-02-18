from django.forms import ModelForm
from crm import models

class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"   #所有字段



