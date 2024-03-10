"""
admin for Profile & ColleagueRequest
"""

from django.contrib import admin
from .models import Profile, ColleagueRequest

admin.site.register(Profile)
admin.site.register(ColleagueRequest)
