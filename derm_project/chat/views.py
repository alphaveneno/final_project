"""
chat room views
"""
from django.shortcuts import render


def room(request, room_name):
    """
    the view for all chat rooms
    """
    return render(request, "chat/room.html", {"room_name": room_name})
