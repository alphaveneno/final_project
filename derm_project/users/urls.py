"""
URLs for users views and APIs
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

# from django.views.generic import TemplateView
# from rest_framework.schemas import get_schema_view
from . import api

urlpatterns = [
    # URLs related to user & profile concerns
    path("edit-profile/", user_views.edit_profile, name="edit_profile"),
    path("my-profile/", user_views.my_profile, name="my_profile"),
    path("users/", user_views.users_list, name="users_list"),
    path("users/<slug>/", user_views.profile_view, name="profile_view"),
    path("search_users/", user_views.search_users, name="search_users"),
    # URLs related to colleagues concerns
    path("colleagues/", user_views.colleague_list, name="colleague_list"),
    path(
        "users/colleague-request/send/<int:id>/",
        user_views.send_colleague_request,
        name="send_colleague_request",
    ),
    path(
        "users/colleague-request/cancel/<int:id>/",
        user_views.cancel_colleague_request,
        name="cancel_colleague_request",
    ),
    path(
        "users/colleague-request/accept/<int:id>/",
        user_views.accept_colleague_request,
        name="accept_colleague_request",
    ),
    path(
        "users/colleague-request/delete/<int:id>/",
        user_views.delete_colleague_request,
        name="delete_colleague_request",
    ),
    path(
        "users/colleague/delete/<int:id>/",
        user_views.delete_colleague,
        name="delete_colleague",
    ),
    # URLs related to user permissions (registration, login, password)
    path("register/", user_views.register, name="register"),
    path(
        "",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # URLs related to APIs
    path("api/profile/<int:pk>", api.ProfileDetail.as_view(), name="profile_api"),
    path("api/profiles/", api.ProfileList.as_view(), name="profiles_api"),
    path(
        "api/colleaguerequest/<int:pk>",
        api.ColleagueRequestDetail.as_view(),
        name="colleaguerequest_api",
    ),
    path(
        "api/colleaguerequests/",
        api.ColleagueRequestList.as_view(),
        name="colleaguerequests_api",
    ),
    # the APIs
    path("api/profile/<int:pk>", api.ProfileDetail.as_view(), name="profile_api"),
    path("api/profiles/", api.ProfileList.as_view(), name="profiles_api"),
    path("api/colleaguerequestdetail/<int:pk>", api.ColleagueRequestDetail.as_view(), name="colleaguerequestdetail_api"),
    path("api/colleaguerequestlist/", api.ColleagueRequestList.as_view(), name="colleaguerequestlist_api"),
]
