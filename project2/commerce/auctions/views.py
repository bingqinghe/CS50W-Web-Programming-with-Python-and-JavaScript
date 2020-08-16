from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist, Category, Winner


def index(request):
    lists = Listing.objects.all()

    try:
        watchlists = Watchlist.objects.filter(user=request.user.username)
        wlcount = len(watchlists)
    except:
        wlcount = None
    return render(request, "auctions/index.html", {
            "lists": lists, "wlcount": wlcount
        })

def categorylist(request):
    lists = Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")

    try:
        watchlists = Watchlist.objects.filter(user=request.user.username)
        wlcount = len(watchlists)
    except:
        wlcount = None
    return render(request, "auctions/categorylist.html", {
            "lists": lists, "wlcount": wlcount
        })

def categoryitem(request, category):
    lists = Listing.objects.filter(category=category)

    try:
        watchlists = Watchlist.objects.filter(user=request.user.username)
        wlcount = len(watchlists)
    except:
        wlcount = None
    return render(request, "auctions/categoryitem.html", {
            "lists": lists, "category": category.upper(), "wlcount": wlcount
        })

def create(request):
    try:
        watchlists = Watchlist.objects.filter(user=request.user.username)
        wlcount = len(watchlists)
    except:
        wlcount = None
    return render(request, "auctions/create.html", {
            "wlcount": wlcount
        })

def submitlist(request):
    if request.method == "POST":
        lists = Listing()
        current = datetime.now().strftime(" %d %B %Y %X ")
        lists.owner = request.user.username
        lists.title = request.POST.get('title')
        lists.description = request.POST.get('description')
        lists.price = request.POST.get('price')
        lists.category = request.POST.get('category')
        lists.time = current
        if request.POST.get('link'):
            lists.link = request.POST.get('link')
        else:
            lists.link = "https://cdn4.iconfinder.com/data/icons/storeage-box/100/DPid-ICONS-61-512.png"
        lists.save()

        catlist = Category()
        items = Listing.objects.all()
        for item in items:
            try:
                if Category.objects.get(listid=item.id):
                    pass
            except:
                catlist.listid = item.id
                catlist.title = item.title
                catlist.description = item.description
                catlist.link = item.link
                catlist.save()

        return redirect('index')
    
    else:
        return redirect("index")

def listingpage(request, id):
    try:
        lists = Listing.objects.get(id=id)
    except:
        return redirect('index')

    try:
        comments = Comment.objects.filter(listid=id)
    except:
        comments = None

    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username, listid=id):
                wladded = True
        except:
            wladded = False

        try:
            getlist = Listing.objects.get(id=id)
            if getlist.owner == request.user.username:
                owner = True
            else:
                owner = False
        except:
            return redirect('index')
    else:
        wladded = False
        owner = False

    try:
        watchlists = Watchlist.objects.filter(user=request.user.username)
        wlcount = len(watchlists)
    except:
        wlcount = None

    return render(request, "auctions/listing.html", {
        "lists": lists, "comments": comments, "owner": owner, "wladded": wladded, "wlcount": wlcount,
        "error": request.COOKIES.get('error'),
        "errorgreen": request.COOKIES.get('errorgreen') 
        })

def removewatchlist(request, listid):
    if request.user.username:
        try:
            watchlists = Watchlist.objects.get(user=request.user.username, listid=listid)
            watchlists.delete()
            return redirect('listingpage', id=listid)
        except:
            return redirect('listingpage', id=listid)
    else:
        return redirect('index')

def addwatchlist(request, listid):
    if request.user.username:
        watchlists = Watchlist()
        watchlists.user = request.user.username
        watchlists.listid = listid
        watchlists.save()
        return redirect('listingpage', id=listid)
    else:
        return redirect('index')

def closebid(request, listid):
    if request.user.username:
        try:
            lists = Listing.objects.get(id=listid)
        except:
            return redirect('index')

        """ Bid on list """
        closed_bid = Winner()
        closed_bid.owner = lists.owner
        closed_bid.listid = listid
        title = lists.title
        try:
            thisbid = Bid.objects.get(listid=listid, price=lists.price)
            closed_bid.winner = thisbid.user
            closed_bid.price = thisbid.price
            closed_bid.save()
            thisbid.delete()
        except:
            closebid.winner = lists.owner
            closed_bid.price = lists.price
            closed_bid.save()

        """ Watchlist """
        try:
            if Watchlist.objects.filter(listid=listid):
                thiswl = Watchlist.objects.filter(listid=listid)
                thiswl.delete()
            else:
                pass
        except:
            pass

        """ Comment """
        try:
            thiscmt = Comment.objects.filter(listid=listid)
            thiscmt.delete()
        except:
            pass

        """ Bid """
        try:
            deletebid = Bid.objects.filter(listid=listid)
            deletebid.delete()
        except:
            pass

        """ Winner """
        try:
            thiswinner = Winner.objects.get(listid=listid)
        except:
            closed_bid.owner = lists.owner
            closed_bid.listid = listid
            closed_bid.winner = lists.owner
            closed_bid.price = lists.price
            closed_bid.save()
            thiswinner = Winner.objects.get(listid=listid)
        lists.delete()

        try:
            watchlists = Watchlist.objects.filter(user=request.user.username)
            wlcount = len(watchlists)
        except:
            wlcount = None

        return render(request, "auctions/winning.html", {
            "title": title, "thiswinner": thiswinner, "wlcount": wlcount
            })
    else:
        return redirect('index')

def submitbid(request, listid):
    current_bid = Listing.objects.get(id=listid).price
    if request.method == 'POST':
        user_bid = int(request.POST.get('bid'))
        if user_bid < current_bid:
            response = redirect('listingpage', id=listid)
            response.set_cookie('error', 'Your bid should be greater than the current bid', max_age=3)
            return response
        else:
            lists = Listing.objects.get(id=listid)
            lists.price = user_bid
            lists.save()
            try:
                if Bid.objects.filter(id=listid):
                    thisbid = Bid.objects.filter(id=listid)
                    thisbid.delete()
                savebid = Bid()
                savebid.user = request.user.username
                savebid.listid = listid
                savebid.title = lists.title
                savebid.price = user_bid
                savebid.save()
            except:
                savebid = Bid()
                savebid.user = request.user.username
                savebid.listid = listid
                savebid.title = lists.title
                savebid.price = user_bid
                savebid.save()
            response = redirect('listingpage', id=listid)
            response.set_cookie('errorgreen', 'Successful Bid', max_age=3)
            return response
    else:
        return redirect('index')

def submitcomment(request, listid):
    if request.method == 'POST':
        current = datetime.now()
        currentime = current.strftime(" %d %B %Y %X ")
        comments = Comment()
        comments.user = request.user.username
        comments.listid = listid
        comments.comment = request.POST.get('comment')
        comments.time = currentime
        comments.save()
        return redirect('listingpage', id=listid)
    else:
        return redirect('index')

def watchlistpage(request, username):
    if request.user.username:
        try:
            watchlists = Watchlist.objects.filter(user=username)
            lists =[]
            for wl in watchlists:
                lists.append(Listing.objects.filter(id=wl.listid))
            try:
                watchlists = Watchlist.objects.filter(user=request.user.username)
                wlcount = len(watchlists)
            except:
                wlcount = None
            return render(request, 'auctions/watchlist.html', {
                "lists": lists, 'wlcout': wlcount
                })
        except:
            try:
                watchlists = Watchlist.objects.filter(user=request.user.username)
                wlcount = len(watchlists)
            except:
                wlcount = None
            return render(request, 'auctions/watchlist.html', {
                "lists": None, 'wlcount': wlcount
                })
    else:
        return redirect('index')

def mywinning(request):
    if request.user.username:
        lists = []
        try:
            winninglist = Winner.objects.filter(winner=request.user.username)
            for winners in winninglist:
                lists.append(Category.objects.filter(listid=winners.listid))
        except:
            winninglist = None
            lists = None

        try:
            watchlists = Watchlist.objects.filter(user=request.user.username)
            wlcount = len(watchlists)
        except:
            wlcount = None

        return render(request, "auctions/mywinning.html", {
            "lists": lists, "winninglist": winninglist, "wlcount": wlcount
            })
    else:
        return redirect('index')
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
