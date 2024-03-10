"""
admin for skin_support app
responsible for posting concerns
"""
from django.contrib import admin
from .models import Post, Comments, Endorse, Vote

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Endorse)
admin.site.register(Vote)
