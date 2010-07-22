from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'social.views',
    url(r'^add_friend/(?P<user_id>\d+)/$', 'add_friend', name='social_add_friend'),
)
