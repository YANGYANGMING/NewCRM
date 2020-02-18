from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def acc_login(request):

    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            print("passed authentication")
            login(request, user)  #把user封装到request.session中
            return redirect(request.GET.get('next', '/'))  #登录后跳转至next指定的页面，否则到首页/
        else:
            error_msg = "Wrong username or password!"

    return render(request, 'login.html', locals())


def acc_logout(request):
    # request.session.clear()
    logout(request)
    return redirect('/login/')










