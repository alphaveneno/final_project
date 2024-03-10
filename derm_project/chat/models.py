"""
model intended for saving messages
"""
# from django.db import models
# from django.contrib.auth.models import User

# class Message(models.Model):
#     """
#     save chat messages here
#     """
#     author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
#     content = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.author.username

#     def last_20_messages(self):
#         """
#         display last 20 messages
#         """
#         return Message.objects.order_by('-timestamp').all()[:20]
