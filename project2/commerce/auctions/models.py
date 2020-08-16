from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
	owner = models.CharField(max_length=64)
	title = models.CharField(max_length=64)
	description = models.TextField()
	price = models.IntegerField()
	category = models.CharField(max_length=64)
	link = models.CharField(max_length=128, default=None, blank=True, null=True)
	time = models.CharField(max_length=64)

class Bid(models.Model):
	user = models.CharField(max_length=64)
	listid = models.IntegerField()
	title = models.CharField(max_length=64)
	price = models.IntegerField()

class Comment(models.Model):
	user = models.CharField(max_length=64)
	listid = models.IntegerField()
	comment = models.TextField()
	time = models.CharField(max_length=64)

class Watchlist(models.Model):
	user = models.CharField(max_length=64)
	listid = models.IntegerField()

class Category(models.Model):
	listid = models.IntegerField()
	title = models.CharField(max_length=64)
	description = models.TextField()
	link = models.CharField(max_length=128, default=None, blank=True, null=True)

class Winner(models.Model):
	owner = models.CharField(max_length=64)
	listid = models.IntegerField()
	winner = models.CharField(max_length=64)
	price = models.IntegerField()
