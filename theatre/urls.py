from django.urls import include, path
from rest_framework.routers import DefaultRouter

from theatre.views import GenreViewSet, ActorViewSet, PlayViewSet, TheatreHallViewSet, PerformanceViewSet, \
    ReservationViewSet

app_name = "theatre"

router = DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]