from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^add-friend/(?P<user_id>\d+)/$', 'social.views.add_friend', name='social_add_friend'),
    url(r'^remove-friend/(?P<user_id>\d+)/$', 'social.views.remove_friend', name='social_remove_friend'),
    url(r'^invitation-confirm/done/$', 'social.views.invitation_confirm_done', name='social_invitation_confirm_done'),
    url(r'^invitation-confirm/(?P<invitation_id>\d+)/$', 'friends.views.respond_to_friendship_invitation', {'redirect_to_view': 'social_invitation_confirm_done'}, name='social_invitation_confirm'),
)
