from django.db import models
from core.models import Profile
# Create your models here.




class Chat(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="message_group_id")
    sender = models.CharField(max_length=8) # user/manager
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat/images/', null=True, blank=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    def last_chat_group():
        data = []
        for x in Chat.objects.order_by('sent_at'):
            is_unique = True
            if len(data) >= 10:
                break
            for y in range(len(data)):
                if data[y]["profile_id"] == x.profile.uid:
                    is_unique = False
                    break
            if is_unique:
                data.append({
                    "profile_id" : x.profile.uid,
                    "sender" : x.sender,
                    "name" : x.profile.user.email,
                    "message" : x.message,
                    "image" : x.image,
                    "sent_at" : x.sent_at
                })

        return data
    def __str__(self) -> str:
        return self.profile.full_name