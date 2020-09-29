from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def get_profile_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.id, filename)

def get_post_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.author.id, filename)

class User_Ex(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile = models.ImageField(upload_to=get_profile_path, default='default.jpg')
	following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class Post(models.Model):
	author = models.ForeignKey(User_Ex, on_delete=models.CASCADE, related_name='user_posts')
	image = models.ImageField(upload_to=get_post_path)
	title = models.TextField()
	preview = models.TextField()
	receipt = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User_Ex, related_name='liked_posts')
	comments = models.ManyToManyField('Comment', related_name='commented_posts')

class Comment(models.Model):
	author = models.ForeignKey(User_Ex, on_delete=models.CASCADE, related_name='user_comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
	comments = models.TextField()
	time = models.DateTimeField(auto_now_add=True)