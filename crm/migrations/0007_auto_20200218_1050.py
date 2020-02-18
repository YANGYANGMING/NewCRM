# Generated by Django 2.2.2 on 2020-02-18 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20200218_1005'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='classlist',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='classlist',
            name='contract_template',
        ),
        migrations.RemoveField(
            model_name='classlist',
            name='course',
        ),
        migrations.RemoveField(
            model_name='classlist',
            name='teachers',
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='courserecord',
            name='class_grade',
        ),
        migrations.RemoveField(
            model_name='courserecord',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='customerfollowup',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customerfollowup',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customerinfo',
            name='consult_courses',
        ),
        migrations.RemoveField(
            model_name='customerinfo',
            name='consultant',
        ),
        migrations.RemoveField(
            model_name='customerinfo',
            name='referral_from',
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='paymentrecord',
            name='consultant',
        ),
        migrations.RemoveField(
            model_name='paymentrecord',
            name='enrollment',
        ),
        migrations.RemoveField(
            model_name='role',
            name='menus',
        ),
        migrations.RemoveField(
            model_name='crm',
            name='class_grades',
        ),
        migrations.RemoveField(
            model_name='crm',
            name='customer',
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='class_grade',
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='consultant',
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='studyrecord',
            name='course_record',
        ),
        migrations.RemoveField(
            model_name='studyrecord',
            name='crm',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
        migrations.DeleteModel(
            name='ClassList',
        ),
        migrations.DeleteModel(
            name='ContractTemplate',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='CourseRecord',
        ),
        migrations.DeleteModel(
            name='CustomerFollowUp',
        ),
        migrations.DeleteModel(
            name='CustomerInfo',
        ),
        migrations.DeleteModel(
            name='Menus',
        ),
        migrations.DeleteModel(
            name='PaymentRecord',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='StudentEnrollment',
        ),
        migrations.DeleteModel(
            name='StudyRecord',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]