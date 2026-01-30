from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from user.views import CreateUserView, LoginUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token-auth/", LoginUserView.as_view(), name="token-auth"),
    path("profile/", ManageUserView.as_view(), name="profile"),
    path("api/token/",
         TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"),

]
