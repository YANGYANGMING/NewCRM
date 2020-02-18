from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin
from student import models

print('crm kingadmin.....')

class TestAdmin(BaseKingAdmin):
    list_display = ['name']

site.register(models.Test, TestAdmin)




