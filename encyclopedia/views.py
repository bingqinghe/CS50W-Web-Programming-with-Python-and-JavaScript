from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown

from . import util

markdowner = Markdown()

class Post(forms.Form):
	title = forms.CharField(label="title")
	text = forms.CharField(widget=forms.Textarea(), label="write the post")

class Search(forms.Form):
	searchtitle = forms.CharField()

class Edit(forms.Form):
	text = forms.CharField(widget=forms.Textarea(), label="edit the post")

def index(request):
    entries = util.list_entries()
    searched = []

    if request.method == 'POST':
    	form = Search(request.POST)
    	if form.is_valid():
    		searchtitle = form.cleaned_data["searchtitle"]
    		for i in entries:
    			if searchtitle in entries:
    				contents = util.get_entry(searchtitle)
    				convertcontents = markdowner.convert(contents)
    				return render(request, "encyclopedia/entry.html", 
    					{"title": searchtitle, "content": convertcontents, "form": Search()})
    			if searchtitle.lower() in i.lower():
    				searched.append(i)
    		return render(request, "encyclopedia/search.html", {"searched": searched, "form": Search()})

    	else:
    		return render(request, "encyclopedia/index.html", {"form": form})
    else:
    	return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form": Search()})

def entry(request, title):
	entries = util.list_entries()
	if title in entries:
		contents = util.get_entry(title)
		convertcontents = markdowner.convert(contents)
		return render(request, "encyclopedia/entry.html", {"title": title, "content": convertcontents, "form": Search()})
	else:
		return render(request, "encyclopedia/error.html", {"message": "The requested page was not found.", "form": Search()})


def edit(request, title):
	if request.method == 'GET':
		contents = util.get_entry(title)
		return render(request, "encyclopedia/edit.html", 
			{"title": title, "edit": Edit(initial={"text": contents}), "form": Search()})
	else:
		form = Edit(request.POST)
		if form.is_valid():
			text = form.cleaned_data["text"]
			util.save_entry(title, text)
			contents = util.get_entry(title)
			convertcontents = markdowner.convert(contents)
			return render(request, "encyclopedia/entry.html", {"title": title, "content": convertcontents, "form": Search()})

def create(request):
	if request.method == 'POST':
		form = Post(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			text = form.cleaned_data["text"]
			entries = util.list_entries()
			if title in entries:
				return render(request, "encyclopedia/error.html", {"message": "This page already exists.", "form": Search()})
			else:
				util.save_entry(title, text)
				contents = util.get_entry(title)
				convertcontents = markdowner.convert(contents)
				return render(request, "encyclopedia/entry.html", {"title": title, "content": convertcontents, "form": Search()})
	
	else:
		return render(request, "encyclopedia/create.html", {"post": Post(), "form": Search()})


def randompage(request):
	if request.method == 'GET':
		entries = util.list_entries()
		index = random.randint(0, len(entries)-1)
		randtitle = entries[index]
		contents = util.get_entry(randtitle)
		convertcontents = markdowner.convert(contents)
		return render(request, "encyclopedia/entry.html", {"title": randtitle, "content": convertcontents, "form": Search()})