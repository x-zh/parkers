from django.conf.urls import patterns, url

urlpatterns = patterns(
    'notifier.views',
    # Examples:
    url(r'^$', 'get_notify'),
    url(r'post/$', 'post_notify')
)
