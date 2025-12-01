from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login, logout
from .models import User


def login_index(request):
    if request.method == 'POST':
        if request.POST.get('account') == "join":
            return redirect('users:JoinUrl')

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('users:LoginUrl')
        else:
            return render(request, "login.html", {"error_msg": "ID혹은 비밀번호가 틀림"})

    return render(request,"login.html")

def logout_index(request):
    if request.method == 'POST':
        logout(request)
    return redirect('users:LoginUrl')


def join_index(request):
    if request.method == 'POST':
        if request.POST.get('account') == 'cancel':
            return redirect('users:JoinUrl')

        email = request.POST.get('email')
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password_check = request.POST.get('password_check')

        #아이디 중복 검사
        if User.objects.filter(email=email).exists():
            return render(request, "join.html", {"error_msg":"이미 존재하는 아이디임."})

        #닉네임 중복 검사
        if User.objects.filter(nickname=nickname).exists():
            return render(request, "join.html", {"error_msg":"이미 존재하는 닉네임임."})

        #비밀번호 불일치 검사
        if password != password_check:
            return render(request, "join.html",{"error_msg":"비밀번호가 일치하지않음."})

        #user 생성
        user = User.objects.create_user(
            email=email,
            name=name,
            nickname=nickname,
            password=password
        )

        return redirect('users:LoginUrl')
    return render(request,"join.html")