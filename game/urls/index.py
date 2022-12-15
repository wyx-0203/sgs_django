from django.urls import path, include
from game.views.index import index,acapp


urlpatterns = [
    path("", index, name="index"),
    path("acapp",acapp),
    path("login/", include("game.urls.login.index")),
]
