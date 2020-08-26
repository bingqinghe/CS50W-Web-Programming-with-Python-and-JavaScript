import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import User, Post, Like, Follow


def index(request):
    try:
        posts = Post.objects.all()
        posts = posts.order_by('-time').all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None

    try:
        likeid = []
        likelist = Like.objects.filter(likedby=request.user.username)
        for i in likelist:
            likeid.append(i.postid)
    except:
        likeid = None

    userlist = []
    userlist.append(request.user.username)
    return render(request, "network/index.html", {
            'page_obj': page_obj,
            'likeid': likeid,
            'userlist': userlist
        })

@login_required
def writepost(request):
    if request.user.username:
        return render(request, 'network/writepost.html')
    else:
        return redirect('index')

@csrf_exempt
@login_required
def submitpost(request):
    if request.user.username:
        if request.method == 'POST':
            posts = Post()
            posts.username = request.user
            posts.likes = 0
            posts.content = request.POST.get('content')
            posts.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

def profile(request, urname):
    """ Post """
    try:
        posts = Post.objects.filter(username=urname)
        posts = posts.order_by('-time').all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        posts = None
    """ Follower + Following"""
    try:
        if Follow.objects.filter(username=urname, follower=request.user.username):
            isfollowed = True
        else:
            isfollowed = False
    except:
        isfollowed = False

    try:
        followerlist = Follow.objects.filter(username=urname)
        followercount = followerlist.count()
    except:
        followercount = 0
    try:
        followinglist = Follow.objects.filter(follower=urname)
        followingcount = followinglist.count()
    except:
        followingcount = 0
    """ Likes """
    try:
        likeid = []
        likelist = Like.objects.filter(likedby=request.user.username)
        for i in likelist:
            likeid.append(i.postid)
    except:
        likeid = None

    userlist = []
    userlist.append(request.user.username)
    return render(request, 'network/profile.html', {
            'profilename': urname,
            'isfollowed': isfollowed,
            'following': followingcount,
            'follower': followercount,
            'page_obj': page_obj,
            'likeid': likeid,
            'userlist': userlist
        })

@csrf_exempt
@login_required
def follow(request, name):
    try:
        f = Follow.objects.get(username=name, follower=request.user.username)
    except:
        f = Follow()
        f.username = name
        f.follower = request.user.username
        f.save()
    return redirect('profile', urname=name)

@csrf_exempt
@login_required
def unfollow(request, name):
    try:
        f = Follow.objects.get(username=name, follower=request.user.username)
        f.delete()
    except:
        return redirect('profile', urname=name)
    return redirect('profile', urname=name)

@login_required
def followposts(request):
    try:
        follows = Follow.objects.filter(follower=request.user.username)
        item = []
        items = []
        followusername = []

        for f in follows:
            followusername.append(f.username)

        for f in followusername:
            posts = Post.objects.filter(username=f)
            posts = posts.order_by('-time').all()
            items.append(posts)

        for i in range(0, len(items)):
            item.extend(items[i])

        paginator = Paginator(item, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None

    try:
        likeid = []
        likelist = Like.objects.filter(likedby=request.user.username)
        for i in likelist:
            likeid.append(i.postid)
    except:
        likeid = None

    userlist = []
    userlist.append(request.user.username)
    return render(request, 'network/following.html', {
        'page_obj': page_obj,
        'likeid': likeid,
        'userlist': userlist
    })

@csrf_exempt
def postapi(request, postid):
    try:
        posts = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post Not Found'}, status=404)
    if request.method == 'GET':
        return JsonResponse(posts.serialize())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('username') == request.user.username:
            if data.get('content') is not None:
                posts.content = data['content']
        else:
            return JsonResponse({'error': 'INVALID ACCESS'}, status=404)
        posts.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({'error': 'INVALID REQUEST'}, status=404)

@csrf_exempt
@login_required
def likeapi(request, postid):
    if request.method == 'GET':
        try:
            posts = Like.objects.get(postid=postid, likedby=request.user.username)
            return JsonResponse(posts.serialize())
        except Like.DoesNotExist:
            return JsonResponse({'error': 'Like Not Found'}, status=404)

    elif request.method == 'POST':
        data = json.loads(request.body)
        if request.user.username == data.get('likedby'):
            likelist = Like()
            likelist.postid = data.get('id')
            likelist.likes = data.get('likes')
            likelist.likedby = data.get('likedby')
            likepost = Post.objects.get(id=data.get('id'))
            likepost.likes = data.get('likes')
            likelist.save()
            likepost.save()
            return JsonResponse({'message': 'successful like', 'status': 201}, status=201)
        else:
            return JsonResponse({'error': 'INVALID ACCESS'}, status=404)

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        if request.user.username == data.get('unlikedby'):
            likelist = Like.objects.get(postid=data.get('id'), likedby=data.get('unlikedby'))
            likelist.delete()
            likepost = Post.objects.get(id=data.get('id'))
            likepost.likes = data.get('likes')
            likepost.save()
            return JsonResponse({'message': 'successful unlike', 'status': 201}, status=201)
    else:
        return JsonResponse({'error': 'INVALID REQUEST'}, status=404)

@csrf_exempt
@login_required
def followapi(request, name):
    try:
        if User.objects.get(username=name):
            try:
                followinglist = Follow.objects.filter(follower=name)
                followingcount = followinglist.count()
            except:
                followingcount = 0

            try:
                followerlist = Follow.objects.filter(username=name)
                followercount = followerlist.count()
            except:
                followercount = 0

            try:
                if Follow.objects.filter(username=name, follower=request.user.username):
                    isfollowed = True
                else:
                    isfollowed = False
            except:
                isfollowed = False
    except:
        return JsonResponse({'error': 'User Not Found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'user': name, 'follower': followercount, 'following': followingcount, 'isfollowed': isfollowed})
    else:
        return JsonResponse({'error': 'INVALID ACCESS'}, status=404)
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

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
