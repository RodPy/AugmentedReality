# Routers provide an easy way of automatically determining the URL conf.
from rest_framework import routers
from django.conf.urls import include, url
from api.views import LecturerViewSet , ImageViewSet

router = routers.DefaultRouter()
router.register(r'lectures', LecturerViewSet)
router.register(r'images', ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]