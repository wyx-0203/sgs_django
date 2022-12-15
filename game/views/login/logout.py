from django.http import JsonResponse
from django.contrib.auth import logout


def logout_sgs(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return JsonResponse(
        {
            "result": "success",
        }
    )
