from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models


@login_required
def dashboard(request):

    return render(request, 'crm/dashboard.html')


@login_required
def stu_enrollment(request):
    customers = models.CustomerInfo.objects.all()
    class_list = models.ClassList.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_grade_id")
        enrollment_obj = models.StudentEnrollment.objects.create(
            customer_id=customer_id,
            class_grade_id=class_grade_id,
            consultant_id=request.user.id,
        )


        enrollment_link = "http://localhost:8000/crm/enrollment/%s/" % enrollment_obj.id

    return render(request, "crm/stu_enrollment.html", locals())









