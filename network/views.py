from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post , Follow , Like
from datetime import datetime
import json
from django.http import JsonResponse


def index(request):
    if request.method == "POST":
        text = request.POST['text']
        user = request.user.username
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        Post.objects.create(
            User = user,
            Content = text,
            Date = time,
            likes = 0
        )

        return redirect("/")
    
    p = Paginator(Post.objects.all().order_by("id").reverse(), 10)
    posts = p.get_page(request.GET.get('page'))
    likes = Like.objects.all()
    has_liked = []

    try:
        for like in likes:
            if like.user == request.user.username:
                has_liked.append(like.post)
    except:
        has_liked = []


    return render(request, "network/index.html", {
        "posts": posts,
        "has_liked": has_liked
        
    })
@login_required
@csrf_exempt
def unlike(request, post):
    if request.method == "POST":
        like = Like.objects.get(
            user = request.user.username,
            post = post
        )

        like.delete()
        
        posts = Post.objects.get(pk=post)
        posts.likes = len(Like.objects.all().filter(post=post))
        posts.save()

        return JsonResponse({"message": "disliked!", "likes": len(Like.objects.all().filter(post=post))})

    return redirect("/")

def userpage(request, name):
    usernamecheck = User.objects.all().filter(username=name)

    if len(usernamecheck) == 0:
        return render(request, "network/error.html", {
            "code": "404",
            "error": "user was not found!"
        })
    likes = Like.objects.all()
    has_liked = []

    try:
        for like in likes:
            if like.user == request.user.username:
                has_liked.append(like.post)
    except:
        has_liked = []
    posts = Post.objects.all().filter(User=name).order_by("id").reverse()
    followers = len(Follow.objects.all().filter(followUser = name))
    following = len(Follow.objects.all().filter(currentUser = name))
    is_follower = False
    is_self = False
    p = Paginator(posts, 10)
    posts = p.get_page(request.GET.get('page'))
    if len(Follow.objects.all().filter(currentUser = request.user.username)) == 1:
        is_follower = True
    if name == request.user.username:
        is_self = True

    return render(request, "network/profile.html", {
        "name": name,
        "posts": posts,
        "followers": followers,
        "is_follower": is_follower,
        "is_self": is_self,
        "following": following,
        "has_liked": has_liked
    })

@login_required(login_url='/login')
def follow(request):
    if request.method == "POST":
        Follow.objects.create(
            currentUser = request.user.username,
            followUser = request.POST['user']
        )
        return redirect(f"/user/{request.POST['user']}")
    
    return redirect("/")

@csrf_exempt
def edit(request, post):
    if request.method == "POST":
        post = Post.objects.get(pk=post)
        post.Content = json.loads(request.body)["content"]
        post.save()
        return JsonResponse({"Content": json.loads(request.body)["content"]})

    return redirect("/")

@login_required
@csrf_exempt
def like(request, post):
    if request.method == "POST":
        Like.objects.create(
            user = request.user.username,
            post = post
        )

        posts = Post.objects.get(pk=post)
        posts.likes = len(Like.objects.all().filter(post=post))
        posts.save()

        return JsonResponse({"message": "liked!", "likes": len(Like.objects.all().filter(post=post))})

    return redirect("/")

@login_required(login_url='/login')
def unfollow(request):
    if request.method == "POST":
        Follow.objects.all().filter(currentUser = request.user.username, followUser = request.POST['user']).delete()
        return redirect(f"/user/{request.POST['user']}")
    
    return redirect("/")

@login_required(login_url='/login')
def following(request):
    following1 = Follow.objects.all().filter(currentUser= request.user.username).values_list('followUser', flat=True)
    posts = []
    postsall = Post.objects.all().order_by("id").reverse()
    likes = Like.objects.all()
    has_liked = []

    try:
        for like in likes:
            if like.user == request.user.username:
                has_liked.append(like.post)
    except:
        has_liked = []

    for post in postsall:
        for follower in following1:
            if post.User == follower:
                posts.append(post)

    p = Paginator(posts, 10)
    posts = p.get_page(request.GET.get('page'))

    return render(request, "network/following.html", {
        "posts": posts,
        "has_liked": has_liked
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

