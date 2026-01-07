from django.urls import include, path
from rest_framework.routers import DefaultRouter

from theatre.views import GenreViewSet, ActorViewSet

app_name = "theatre"

router = DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
urlpatterns = [
    path("", include(router.urls)),
]