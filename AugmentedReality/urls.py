from django.conf.urls import patterns, include, url
from django.contrib import admin
from AugmentedReality import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AugmentedReality.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#     url(r'^$', login_required(cache_page(60 * 15)
#         (TemplateView.as_view(template_name="index.html")))),

    url(r'^$', login_required(
        (TemplateView.as_view(template_name="index.html")))),

    url(r'^lectures/$', login_required(
        (TemplateView.as_view(template_name="lectures.html")))),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include('api.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})
        )