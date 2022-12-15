from django.http import JsonResponse
from game.models.player.player import Player


def getinfo_acapp(request):
    player = Player.objects.all()[0]
    return JsonResponse(
        {
            "result": "success",
            "username": player.user.username,
            "photo": player.photo,
        }
    )


def getinfo_web(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"result": "未登录"})
    else:
        player = Player.objects.get(user=user)
        return JsonResponse(
            {
                "result": "success",
                "username": player.user.username,
                "photo": player.photo,
            }
        )


# 获取用户信息
def getinfo(request):
    platform = request.GET.get("platform")
    # ACAPP平台
    if platform == "ACAPP":
        return getinfo_acapp(request)
    # elif platform == "WEB":
    #     return getinfo_web(request)

    # 其他平台
    else:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"result": "未登录"})
        else:

            player = Player.objects.get(user=user)
            return JsonResponse(
                {
                    "result": "success",
                    "username": player.user.username,
                    "portrait": player.portrait,
                }
            )
