from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response
    
from friends.models import FriendshipInvitation


@login_required
def add_friend(request, user_id):
    """
    Ajax view used in conjunction with the friendship_setup_button tag to create a user invitation and return 
    the same tag with updated friend relation.
    """
    if not request.is_ajax():
        raise Http404
    
    user = User.objects.get(id=user_id)
    requesting_user = request.user

    FriendshipInvitation.objects.create_friendship_request(from_user=requesting_user, to_user=user)
   
    return render_to_response('social/inclusion_tags/friendship_awaiting_confirmation_button.html', {'object': user})
