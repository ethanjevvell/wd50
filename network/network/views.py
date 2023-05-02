from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Profile, Post
from .forms import NewPostForm
from .models import User
import json


def index(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewPostForm()

    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'network/index.html', {'form': form, 'posts': posts})


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


def all_posts(request):
    all_posts_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(all_posts_list, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'network/all_posts.html', {'posts': posts})


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = user_profile.profile

    user_posts = Post.objects.filter(user=user_profile).order_by('-timestamp')
    paginator = Paginator(user_posts, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'network/profile.html', {'profile': profile, 'posts': posts})


@login_required
def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    current_user_profile = request.user.profile
    followed_users = current_user_profile.following.all()

    followed_posts = Post.objects.filter(
        user__in=followed_users).order_by('-timestamp')
    paginator = Paginator(followed_posts, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'network/following.html', {'posts': posts})


def like_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    post.save()
    return JsonResponse({"message": "Post liked/unliked successfully."}, status=201)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return JsonResponse({'message': 'Post updated successfully'})
    else:
        return render(request, 'network/edit_post.html', {'post': post})


@login_required
def follow(request, username):
    if request.method == 'GET':
        user_to_follow = get_object_or_404(User, username=username)
        current_user_profile = request.user.profile

        if user_to_follow == request.user:
            return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

        current_user_profile.following.add(user_to_follow)
        user_to_follow.profile.followers.add(request.user)

        current_user_profile.save()
        user_to_follow.profile.save()

        return HttpResponseRedirect(reverse('profile', args=[user_to_follow.username]))

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def unfollow(request, username):
    if request.method == 'GET':
        user_to_unfollow = get_object_or_404(User, username=username)
        current_user_profile = request.user.profile

        if user_to_unfollow == request.user:
            return JsonResponse({'error': 'You cannot unfollow yourself'}, status=400)

        current_user_profile.following.remove(user_to_unfollow)
        user_to_unfollow.profile.followers.remove(request.user)

        current_user_profile.save()
        user_to_unfollow.profile.save()

        return HttpResponseRedirect(reverse('profile', args=[user_to_unfollow.username]))

    return JsonResponse({'error': 'Invalid request method'}, status=400)
