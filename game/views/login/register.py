from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from game.models.player.player import Player



def register(request):
    data = request.GET
    # 若不存在则返回空字符串，strip去空格
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    password_confirm = data.get("confirmPassword", "").strip()
    if not username or not password:
        return JsonResponse({
            'result': "用户名或密码不能为空！"
        })
    if password != password_confirm:
        return JsonResponse({
            'result': "两次密码不一致！",
        })
    # filter查找数据库
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'result': "用户名已存在！"
        })
    user = User(username=username)
    user.set_password(password)
    user.save()
    Player.objects.create(user=user, portrait="https://web.sanguosha.com/10/pc/res/assets/runtime/general/big/static/100201.png")
    login(request, user)
    return JsonResponse({
        'result': "success",
    })
