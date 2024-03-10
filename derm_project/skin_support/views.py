"""
user views
"""
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import NewCommentForm, NewPostForm
from .models import Post, Endorse, Comments, Vote


class PostListView(ListView):
    """
    lists all posts on the home page, most recent near top
    """

    model = Post
    template_name = "skin_support/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        context data returned
        """
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            endorsed = [
                i
                for i in Post.objects.all()
                if Endorse.objects.filter(user=self.request.user, post=i)
            ]
            context["endorsed_post"] = endorsed
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    """
    lists an author's posts,
    accessed when author's name clicked on
    """

    model = Post
    template_name = "skin_support/user_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        context data
        """
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        endorsed = [
            i
            for i in Post.objects.filter(user_name=user)
            if Endorse.objects.filter(user=self.request.user, post=i)
        ]
        context["endorsed_post"] = endorsed
        return context

    def get_queryset(self):
        """
        get post queryset for list
        """
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(user_name=user).order_by("-date_posted")


@login_required
def post_detail(request, pk):
    """
    detail for adding comments to posts
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_endorsed = Endorse.objects.filter(user=user, post=post)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect("post-detail", pk=pk)
    else:
        form = NewCommentForm()
    return render(
        request,
        "skin_support/post_detail.html",
        {"post": post, "is_endorsed": is_endorsed, "form": form},
    )


@login_required
def create_post(request):
    """
    create a new post
    """
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request, "Posted Successfully")
            return redirect("home")
    else:
        form = NewPostForm()
    return render(request, "skin_support/create_post.html", {"form": form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    update a post
    """

    model = Post
    fields = fields = [
        "age",
        "gender",
        "ethnicity",
        "history",
        "country",
        "skin_location",
        "provdx",
        "ddx1",
        "ddx2",
        "pic1",
        "pic2",
        "pic3",
        "tags",
    ]
    template_name = "skin_support/create_post.html"

    def form_valid(self, form):
        """
        check form validity
        """
        form.instance.user_name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        affirm request is from the user
        """
        post = self.get_object()
        if self.request.user == post.user_name:
            return True
        return False


@login_required
def post_delete(request, pk):
    """
    delete a post
    """
    post = Post.objects.get(pk=pk)
    if request.user == post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect("home")


@login_required
def search_posts(request):
    """
    when on a page dealing with posts,
    the search bar displays 'search posts'
    and enables searches for posts
    o/w it enables searches for users
    and displays 'search users'
    """
    query = request.GET.get("p")
    object_list = Post.objects.filter(tags__icontains=query)
    endorsed = [
        i for i in object_list if Endorse.objects.filter(user=request.user, post=i)
    ]
    context = {"posts": object_list, "endorsed_post": endorsed}
    return render(request, "skin_support/search_posts.html", context)


@login_required
def endorse(request):
    """
    allows the user to endorse or unendorse a post
    an 'endorse' of a post is stored in the Endorse model
    """
    try:
        post_id = request.GET.get("endorseId", "")
        user = request.user
        post = Post.objects.get(pk=post_id)
        endorsed = False

        # the user must not endorse his own post
        endorse = Endorse.objects.filter(user=user, post=post)
        if endorse:
            endorse.delete()
        else:
            endorsed = True
            Endorse.objects.create(user=user, post=post)

        # get the number of endorses for the post
        endorses = Endorse.objects.filter(post=post).count()
        resp = {"endorsed": endorsed, "endorses": endorses}
        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json")
    except ValueError:
        print("ValueError: post_id is an empty string ")
        return HttpResponseRedirect("/home")


@login_required
def vote(request):
    """
    allows the user to upvote or downvote a comment
    votes on a comment is stored in the Vote model
    """
    try:
        vote_id = request.GET.get("voteId", "")
        user = request.user
        comment = Comments.objects.get(pk=vote_id)
        upvoted = False

        # user must not upvote his own comment
        upvote = Vote.objects.filter(user=user, comment=comment)
        if upvote:
            upvote.delete()
        else:
            upvoted = True
            Vote.objects.create(user=user, comment=comment)

        # get the number of upvotes for the comment
        upvotes = Vote.objects.filter(comment=comment).count()
        resp = {"upvoted": upvoted, "upvotes": upvotes}
        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json")
    except ValueError:
        print("ValueError: vote_id is an empty string ", vote_id)
        return HttpResponseRedirect("/home")


def about(request):
    """
    displays the 'about" page
    """
    return render(request, "skin_support/about.html", {"title": "About"})
