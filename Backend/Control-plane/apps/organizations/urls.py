from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("", OrganizationViewSet, basename="organization")

urlpatterns = router.urls
