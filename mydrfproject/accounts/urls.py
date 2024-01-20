
from django.urls import path
from .views import register_user, user_login, search_users, send_friend_request, accept_friend_request, reject_friend_request, list_friends, list_pending_friend_requests


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('search/', search_users, name='search_users'),
    path('friend-request/send/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-request/accept/<int:friend_request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:friend_request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends/', list_friends, name='list_friends'),
    path('friend-requests/pending/', list_pending_friend_requests, name='list_pending_friend_requests'),
]