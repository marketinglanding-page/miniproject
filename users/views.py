from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login, logout
from .models import UserDB

def login_index(request):
    if request.method == 'POST':
        account = request.POST.get('account')

        if account == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            userObject = authenticate(username=username, password=password)

            if userObject is not None:
                login(request, userObject)

            else:
                print('실패하였습니다.')
        else:
            return redirect('users:JoinUrl')
    else:
        pass

    return render(request, 'login.html', { })

def logout_index(request):
    logout(request)
    return redirect('users:LoginUrl')


def join_index(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        print(account)

        if account == 'create':
            new_username = request.POST.get('username')
            new_password = request.POST.get('password')
            new_password_check = request.POST.get('password_check')
            print(new_username)
            print(new_password)

            # 예외처리1 (ID 아니면 비밀번호가 완성 X)
            if not new_username or not new_password:
                return render(request, 'join.html', {'error_msg' : '아이디 또는 비밀번호를 입력하시오.'})

            # 예외처리2 (비밀번호 확인에서 에러)
            elif new_password != new_password_check:
                return render(request, 'join.html', {'error_msg' : '비밀번호가 서로 맞지않습니다.'})

            #예외처리 3 (아이디중복)
            elif UserDB.objects.filter(username=new_username).exists():
                return render(request, 'join.html', {'error_msg' : '이미 사용중인 아이디임.'})

            # 이상 무
            new_users = UserDB.objects.create_user(username=new_username, password=new_password)
            new_users.save()
        else:
            pass

        return redirect('users:LoginUrl')

    return render(request,'join.html', {})