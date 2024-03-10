"""
user views
"""
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from skin_support.models import Post
from .models import Profile, ColleagueRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@login_required
def users_list(request):
    """
    shows the user a list of people
    who are not yet his colleagues
    """
    users = Profile.objects.exclude(user=request.user)
    sent_colleague_requests = ColleagueRequest.objects.filter(from_user=request.user)
    my_colleagues = request.user.profile.colleagues.all()
    colleagues = []
    sent_to = []

    # 'colleagues' is a list of users to be invited as colleagues
    for user in my_colleagues:
        colleague = user.colleagues.all()
        colleagues = [c for c in colleague for c in colleague.exclude(user=c.user)]

    my_colleagues = request.user.profile.colleagues.all()
    colleagues = list(set(colleagues) - set(my_colleagues))

    if request.user.profile in colleagues:
        colleagues.remove(request.user.profile)

    # samples a limited number(10) of random registered members
    # who are not already colleagues
    # to recommend for colleague requests
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in colleagues:
            random_list.remove(r)
    colleagues += random_list
    for i in my_colleagues:
        if i in colleagues:
            colleagues.remove(i)
    colleagues = list(set(colleagues))
    for se in sent_colleague_requests:
        sent_to.append(se.to_user)
    context = {"users": colleagues, "sent": sent_to}
    return render(request, "users/users_list.html", context)


@login_required
def colleague_list(request):
    """
    the list the user sees when he clicks on 'Colleagues'
    """
    # make sure user has a profile
    if getattr(request.user, "profile", None):
        p = request.user.profile
        colleagues = p.colleagues.all()
    context = {"colleagues": colleagues}
    return render(request, "users/colleague_list.html", context)


@login_required
def send_colleague_request(request, id):
    """
    send a colleague request via HTTP
    request is saved in ColleagueRequest model
    """
    user = get_object_or_404(User, id=id)
    ColleagueRequest.objects.get_or_create(from_user=request.user, to_user=user)
    return HttpResponseRedirect("/users")


@login_required
def cancel_colleague_request(request, id):
    """
    cancel colleague request by deleting it from
    ColleagueRequest model
    """
    user = get_object_or_404(User, id=id)
    frequest = ColleagueRequest.objects.filter(
        from_user=request.user, to_user=user
    ).first()
    frequest.delete()
    return HttpResponseRedirect("/users")


@login_required
def delete_colleague_request(request, id):
    """
    'delete_colleague_request' same idea as 'cancel_colleague_request'
    looks for and deletes any entry in ColleagueRequests model
    that is the reciprocal of the one deleted in 'cancel_colleague_request'
    """
    from_user = get_object_or_404(User, id=id)
    frequest = ColleagueRequest.objects.filter(
        from_user=from_user, to_user=request.user
    ).first()
    frequest.delete()
    return HttpResponseRedirect(f"/users/{request.user.profile.slug}")


@login_required
def accept_colleague_request(request, id):
    """
    accept colleague request via HTTP,
    request can be deleted from ColleagueRequest model
    and a ManyToMany relationship
    established in Profile.
    """
    from_user = get_object_or_404(User, id=id)
    frequest = ColleagueRequest.objects.filter(
        from_user=from_user, to_user=request.user
    ).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.colleagues.add(user2.profile)
    user2.profile.colleagues.add(user1.profile)
    if ColleagueRequest.objects.filter(
        from_user=request.user, to_user=from_user
    ).first():
        request_rev = ColleagueRequest.objects.filter(
            from_user=request.user, to_user=from_user
        ).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect(f"/users/{request.user.profile.slug}")


def delete_colleague(request, id):
    """
    remove the ManyToMany relationship
    """
    user_profile = request.user.profile
    colleague_profile = get_object_or_404(Profile, id=id)
    user_profile.colleagues.remove(colleague_profile)
    colleague_profile.colleagues.remove(user_profile)
    return HttpResponseRedirect(f"/users/{colleague_profile.slug}")


@login_required
def profile_view(request, slug):
    """
    this is the view the user sees of someone elses' profile
    when he clicks on their name on the home page
    the 'context' object (see below) shows the info,
    besides the profile, to be displayed
    """
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_colleague_requests = ColleagueRequest.objects.filter(from_user=p.user)
    rec_colleague_requests = ColleagueRequest.objects.filter(to_user=p.user)

    user_posts = Post.objects.filter(user_name=u)

    colleagues = p.colleagues.all()

    # is this user our colleague?
    button_status = "none"
    if p not in request.user.profile.colleagues.all():
        button_status = "not_colleague"

        # if we have sent him a colleague request
        if (
            len(
                ColleagueRequest.objects.filter(from_user=request.user).filter(
                    to_user=p.user
                )
            )
            == 1
        ):
            button_status = "colleague_request_sent"

        # if we have received a colleague request
        if (
            len(
                ColleagueRequest.objects.filter(from_user=p.user).filter(
                    to_user=request.user
                )
            )
            == 1
        ):
            button_status = "colleague_request_received"

    context = {
        "u": u,
        "button_status": button_status,
        "colleagues_list": colleagues,
        "sent_colleague_requests": sent_colleague_requests,
        "rec_colleague_requests": rec_colleague_requests,
        "post_count": user_posts.count,
    }

    return render(request, "users/profile.html", context)


@login_required
def search_users(request):
    """
    for the user search bar
    """
    query = request.GET.get("q")
    object_list = User.objects.filter(username__icontains=query)
    context = {"users": object_list}
    return render(request, "users/search_users.html", context)


############################################################################################


def register(request):
    """
    registration:
    user is redirected to login page
    if successful
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"{username}, your account has been created! You can now login!",
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def edit_profile(request):
    """
    link to this page is on user's profile page
    crispy-forms for User and for Profile are combined
    """
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("my_profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/edit_profile.html", context)


@login_required
def my_profile(request):
    """
    the user's own profile page
    """
    button_status = "none"
    colleagues = []
    sent_colleague_requests = []
    rec_colleague_requests = []
    user_posts = []
    you = ""

    # make sure user has a profile
    if getattr(request.user, "profile", None):
        p = request.user.profile
        you = p.user
        sent_colleague_requests = ColleagueRequest.objects.filter(from_user=you)
        rec_colleague_requests = ColleagueRequest.objects.filter(to_user=you)
        user_posts = Post.objects.filter(user_name=you)
        colleagues = p.colleagues.all()

        # is this user our colleague ?

        if p not in request.user.profile.colleagues.all():
            button_status = "not_colleague"

            # if we have sent him a colleague request
            if (
                len(
                    ColleagueRequest.objects.filter(from_user=request.user).filter(
                        to_user=you
                    )
                )
                == 1
            ):
                button_status = "colleague_request_sent"

            if (
                len(
                    ColleagueRequest.objects.filter(from_user=p.user).filter(
                        to_user=request.user
                    )
                )
                == 1
            ):
                button_status = "colleague_request_received"

    # in addition to the user's profile,
    # info re: his # of posts, # of colleagues
    # & current colleague requests
    # is returned to be displayed
    context = {
        "u": you,
        "button_status": button_status,
        "colleague_list": colleagues,
        "sent_colleague_requests": sent_colleague_requests,
        "rec_colleague_requests": rec_colleague_requests,
        "post_count": user_posts.count(),
    }

    return render(request, "users/profile.html", context)
