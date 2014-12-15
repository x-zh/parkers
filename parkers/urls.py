from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

from backend import views as v

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    url(r'^query/', include('query.urls')),
    url(r'^notifier/', include('notifier.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^google_map/$', v.google_map),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
