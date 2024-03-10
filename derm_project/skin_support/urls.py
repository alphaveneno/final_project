"""
derm_project URLs
"""
from django.urls import path
from . import views
from . import api
from .views import PostUpdateView, PostListView, UserPostListView


urlpatterns = [
    path("home/", PostListView.as_view(), name="home"),
    path("post/new/", views.create_post, name="post-create"),
    path("post/<int:pk>/", views.post_detail, name="post-detail"),
    path("endorse/", views.endorse, name="post-endorse"),
    path("vote/", views.vote, name="comment-vote"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post-delete"),
    path("search_posts/", views.search_posts, name="search_posts"),
    path("user_posts/<str:username>", UserPostListView.as_view(), name="user_posts"),
    # this page opens with 'http://localhost:800x/about'
    path("about/", views.about, name="about"),
    # the APIs
    path("api/post/<int:pk>", api.PostDetail.as_view(), name="post_api"),
    path("api/posts/", api.PostList.as_view(), name="posts_api"),
    path("api/comment/<int:pk>", api.CommentsDetail.as_view(), name="comment_api"),
    path("api/comments/", api.CommentsList.as_view(), name="comments_api"),
    path("api/endorse/<int:pk>", api.EndorseDetail.as_view(), name="endorse_api"),
    path("api/endorses/", api.EndorseList.as_view(), name="endorses_api"),
    path("api/vote/<int:pk>", api.VoteDetail.as_view(), name="vote_api"),
    path("api/votes/", api.VoteList.as_view(), name="votes_api"),
]
