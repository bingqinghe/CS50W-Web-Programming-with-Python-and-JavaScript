from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
	username = models.CharField(max_length=64)
	likes = models.IntegerField()
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		return {
			'id': self.id,
			'username': self.username,
			'likes': self.likes,
			'content': self.content,
			'time': self.time.strftime(' %b %d %Y, %H:%M:%S ')
		}

class Like(models.Model):
	postid = models.IntegerField()
	likes = models.IntegerField()
	likedby = models.CharField(max_length=64)

	def serialize(self):
		return {
			'id': self.postid,
			'likes': self.likes,
			'likedby': self.likedby,
		}

class Follow(models.Model):
	username = models.CharField(max_length=64)
	follower = models.CharField(max_length=64)

	def serialize(self):
		return {
			'id': self.id,
			'user': self.username,
			'follower': self.follower
		}