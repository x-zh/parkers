from django.conf.urls import patterns, url

urlpatterns = patterns(
    'query.views',
    # Examples:
    url(r'^$', 'main'),
    url(r'api/$', 'api_call')
)
