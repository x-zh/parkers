from django.conf.urls import patterns, url

from backend import views as v
urlpatterns = patterns('',
                       url(r'^google_map/$', v.google_map),
)