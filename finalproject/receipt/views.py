import uuid, base64, json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from datetime import datetime
from .models import Post, Comment, User_Ex

# Create your views here.
def index(request):
	if request.user.id is None:
		return HttpResponseRedirect(reverse('welcome'))

	user = User.objects.get(id=request.user.id)
	users = User_Ex.objects.get(user__id=user.id)
	info = {
		'posts': [], 
		'following': False
	}
	if users.following.count() > 0:
		info['following'] = True
	for following in users.following.all():
		info['posts'].extend(Post.objects.filter(author__id=following.id))
	info['posts'].sort(key=lambda x: x.time, reverse=True)

	return render(request, 'receipt/index.html', info)

def welcome(request):
	if request.method == 'POST':
		return HttpResponseNotAllowed(['GET'])
	
	return render(request, 'receipt/welcome.html')

def login_view(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])
	
	user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
	if user is None:
		return HttpResponseRedirect(reverse('welcome'))
	
	login(request, user)
	return HttpResponseRedirect(reverse('index'))


def logout_view(request):
	if request.method == 'POST':
		return HttpResponseNotAllowed(['GET'])
	
	logout(request)
	return HttpResponseRedirect(reverse('welcome'))

def register_view(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])

	user = User.objects.create_user(
		username = request.POST['username'],
		email = request.POST['email'],
		password = request.POST['password']
	)
	users = User_Ex.objects.create(
		user = User.objects.get(id=user.id)
	)

	login(request, user)
	return HttpResponseRedirect(reverse('index'))

def profile_view(request, user_id=None):
	if request.method == 'POST':
		return HttpResponseNotAllowed(['GET'])

	if user_id is None:
		if request.user.id is None:
			return HttpResponseRedirect(reverse('welcome'))
		find_id = request.user.id
	else:
		find_id = user_id

	users = User_Ex.objects.get(user__id=find_id)

	show_follow = False
	if user_id is not None and user_id != request.user.id:
		show_follow = True

	followed = False
	if show_follow:
		followed = user_id in [x.user.id for x in User_Ex.objects.get(user__id=request.user.id).following.all()]

	info = {
		'users': users,
		'posts': Post.objects.filter(author__user__id=find_id).order_by('-time'),
		'show_follow_button': show_follow,
		'already_follow': followed,
		'following': users.following.count(),
		'followers': users.followers.count()
	}

	return render(request, 'receipt/user.html', info)

def search(request):
	if request.method == 'POST':
		return HttpResponseNotAllowed(['GET'])
	query = request.GET['searchquery']
	info = {
		'users': User_Ex.objects.filter(user__username__icontains=query),
		'posts': Post.objects.filter(receipt__icontains=query)
	}
	return render(request, 'receipt/search.html', info)

def following_view(request, user_id):
	users = User_Ex.objects.get(user__id=user_id)
	info = {
		'users': users,
		'following': users.following.all()
	}
	return render(request, 'receipt/following.html', info)

def followers_view(request, user_id):
	users = User_Ex.objects.get(user__id=user_id)
	info = {
		'users': users,
		'followers': users.followers.all()
	}
	return render(request, 'receipt/followers.html', info)

def post(request, post_id):
	if request.method == 'POST':
		return HttpResponseNotAllowed(['GET'])

	info = {
		'post': Post.objects.get(id=post_id),
		'comments': Comment.objects.filter(post__id=post_id).order_by('-time')
	}

	user_id = request.user.id
	liked = False
	if user_id is not None and user_id in [x.user.id for x in info['post'].likes.all()]:
		liked = True

	info['user_liked'] = liked
	return render(request, 'receipt/post.html', info)

@login_required
@csrf_exempt
def addfollow(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])

	user_following = User_Ex.objects.get(user__id=request.user.id)
	user_to_follow = User_Ex.objects.get(user__id=request.POST['user_to_follow']);
	user_following.following.add(user_to_follow)

	return JsonResponse({'followers': user_to_follow.followers.count()})

@login_required
@csrf_exempt
def addlike(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])

	postid = request.POST['post_id']
	userid = request.user.id
	post = Post.objects.get(id=postid)
	post.likes.add(User_Ex.objects.get(user__id=userid))

	return JsonResponse({'likes': post.likes.count()})

@login_required
def addcomment(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])

	cmt = request.POST['comment']
	postid = request.POST['post_id']
	comment = Comment.objects.create(
		author = User_Ex.objects.get(user__id=request.user.id),
		post = Post.objects.get(id=postid),
		comments = cmt
		)
	post = Post.objects.get(id=postid)
	post.comments.add(comment)

	cmts = [{
		'author_name': x.author.user.username,
		'author_id': x.author.user.id,
		'time': x.time.strftime(' %b %d %Y, %H:%M:%S '),
		'text': x.comments
	} for x in Comment.objects.filter(post__id=postid).order_by('-time')]

	return JsonResponse({'comments': cmts})

@login_required
@csrf_exempt
def profile_photo(request):
	if request.method == 'GET':
		return HttpResponseNotAllowed(['POST'])

	image_data = request.POST['image']
	format, imgstr = image_data.split(';base64,')
	ext = format.split('/')[-1]
	data = ContentFile(base64.b64decode(imgstr))
	filename = f"{str(uuid.uuid4())}.{ext}"
	users = User_Ex.objects.get(user__id=request.user.id)
	if users.profile != users.profile.field.default:
		users.profile.delete(save=True)
	users.profile.save(filename, data, save=True)

	return JsonResponse({'message': 'succeess'})

@login_required
@csrf_exempt
def upload(request):
	if request.method == 'GET':
		return render(request, 'receipt/upload.html')

	title = request.POST['title']
	preview = request.POST['preview']
	receipt = request.POST['receipt']
	image_data = request.POST['image']
	format, imgstr = image_data.split(';base64,')
	ext = format.split('/')[-1]
	data = ContentFile(base64.b64decode(imgstr))
	filename = f"{str(uuid.uuid4())}.{ext}"
	post = Post.objects.create(
		author = User_Ex.objects.get(user__id=request.user.id),
		title = title,
		preview = preview,
		receipt = receipt
		)
	post.image.save(filename, data, save=True)

	return HttpResponseRedirect(reverse('user'))

