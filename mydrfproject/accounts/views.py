from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import CustomUser, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from datetime import datetime, timedelta


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    keyword = request.GET.get('keyword', '')
    page = int(request.GET.get('page', 1))
    per_page = 10
    start = (page - 1) * per_page
    end = page * per_page

    if '@' in keyword:
        try:
            user = CustomUser.objects.get(email=keyword)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        users = CustomUser.objects.filter(username__icontains=keyword)[start:end]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, to_user_id):
    from_user = request.user

    # Check if the user is trying to send a request to themselves
    if from_user.id == int(to_user_id):
        return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

    to_user = CustomUser.objects.get(pk=to_user_id)

    # Check if a friend request already exists
    if FriendRequest.objects.filter(Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)).exists():
        return Response({'error': 'Friend request already sent or received'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the users are already friends
    if from_user.friends.filter(pk=to_user_id).exists():
        return Response({'error': 'Users are already friends'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has sent too many requests in the last minute
    # recent_requests_count = FriendRequest.objects.filter(from_user=from_user, created_at__gte=timezone.now() - timedelta(minutes=1)).count()
    recent_requests_count = FriendRequest.objects.filter(from_user=from_user, created_at__gte=datetime.now() - timedelta(minutes=1)).count()
    if recent_requests_count >= 3:
        return Response({'error': 'You have reached the limit of friend requests in the last minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    serializer = FriendRequestSerializer(friend_request)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(pk=friend_request_id)

    # Check if the user has permission to accept the friend request
    if friend_request.to_user != request.user:
        return Response({'error': 'You do not have permission to accept this friend request'}, status=status.HTTP_403_FORBIDDEN)

    friend_request.status = 'accepted'
    friend_request.save()
    return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(pk=friend_request_id)

    # Check if the user has permission to reject the friend request
    if friend_request.to_user != request.user:
        return Response({'error': 'You do not have permission to reject this friend request'}, status=status.HTTP_403_FORBIDDEN)

    friend_request.status = 'rejected'
    friend_request.save()
    return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = request.user.friends.all()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_friend_requests(request):
    pending_requests = request.user.received_friend_requests.filter(status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
