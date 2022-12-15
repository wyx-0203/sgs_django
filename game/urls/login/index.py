from django.urls import path, include
from game.views.login.getinfo import getinfo
from game.views.login.login import login_sgs
from game.views.login.logout import logout_sgs
from game.views.login.register import register


urlpatterns = [
    path("getinfo/", getinfo, name="login_getinfo"),
    path("login/", login_sgs, name="login_login"),
    path("logout/", logout_sgs, name="login_logout"),
    path("register/", register, name="login_register"),
    # path("acwing/", include("game.urls.settings.acwing.index")),
]
