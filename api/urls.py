# Routers provide an easy way of automatically determining the URL conf.
from rest_framework import routers
from django.conf.urls import include, url
from api.views import LecturerViewSet , ImageViewSet, ProfileViewSet,\
    UserViewSet, FacebookLogin

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'lectures', LecturerViewSet)
router.register(r'images', ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

]