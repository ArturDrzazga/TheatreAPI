from django.urls import path

from user.views import CreateUserView, LoginUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token-auth/", LoginUserView.as_view(), name="token-auth"),

]
