from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', related_name='friends', blank=True)

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    status_choices = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)