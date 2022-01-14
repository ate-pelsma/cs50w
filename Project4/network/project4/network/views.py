from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm, widgets
from django import forms
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
import json
from django.utils import timezone
from django.forms.models import model_to_dict

from .models import *

MAX_POST_ON_PAGE = 10

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': "",
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': "col-lg-12", 'id': "edit_post", 'cols': 250, 'rows': 3})
        }

class EditPost(forms.Form):
    edit_post_content = forms.Field(widget=forms.Textarea({
        'id': 'post_edit_content', 'rows': 3, 'class': "col-lg-12", 'cols': 250}), required=True)


def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    user = request.user
    for post in all_posts:
        if user in post.likes.all():
            post.liked = True
            post.save()
        else:
            post.liked = False
            post.save()

        print(post.liked)
        
    paginator = Paginator(all_posts, MAX_POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            NewPost = form.save(commit=False)
            NewPost.creator = request.user
            NewPost.save()

            return render(request, "network/index.html", {
                "form": PostForm(),
                "success": True,
                "posts": page_obj
            })

    else:
        return render(request, "network/index.html", {
            "form": PostForm(),
            "form_edit": EditPost(),
            "posts": page_obj
        })

def profile(request, username):

    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(creator=user).order_by('-timestamp')
    following = user.following.all()
    followers = user.followers.all()

    ## Check to see if logged in user is following the visited profile
    is_following = False
    for x in followers:
        if request.user.username == x.follower.username:
            is_following = True

    return render(request, "network/profile.html", {
        "username": username,
        "user_posts": user_posts,
        "following": following,
        "followers": followers,
        "is_following": is_following
    })

def follow_view(request, username):
    follow_user = User.objects.get(username=username)
    user = request.user
    x = Follower(follower=user, following=follow_user)
    x.save()

    return HttpResponseRedirect(reverse("profile", kwargs={'username': username}))

def unfollow_view(request, username):
    unfollow_user = User.objects.get(username=username)
    user = request.user
    target = Follower.objects.filter(follower=user, following=unfollow_user)
    target.delete()

    return HttpResponseRedirect(reverse("profile", kwargs={'username': username}))

def following_posts_view(request):
    ## Find the list of users that the user follows
    user = request.user
    following_users = User.objects.filter(followers__follower=user)
    
    ## Display the posts made by these users
    following_posts = Post.objects.filter(creator__in=following_users).order_by('-timestamp')

    return render(request, "network/following.html", {
        "following_posts": following_posts
    })

def edit(request, id):
    if request.method == "POST":
        try:
            post = Post.objects.get(creator=request.user, pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        body = json.loads(request.body)

        post.content = body.get('content')
        post.save(update_fields=['content'])
        
        return JsonResponse({
            'succes': _("Post edited successfully")
        }, status=200)

    else:
        return JsonResponse({'error': HttpResponseBadRequest("Bad Request")}, status=400)

def like_view(request, id):
    if request.method == "POST":

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            css_style = "far fa-heart"
        else:    
            post.likes.add(user)
            css_style = "fas fa-heart"

        post = Post.objects.get(pk=id)

        total_likes = post.likes.all().count()







        

        return JsonResponse({
            "css_class": css_style,
            "total_likes": total_likes
        })






def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
