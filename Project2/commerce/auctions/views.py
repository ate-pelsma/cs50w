from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from auctions.models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'image']
        labels = {
            'image': _('Image (Optional)'),
            'category': _('Category (Optional)'),
        }
        help_texts = {
            'image': _('Copy the URL to your image in the field above'),
            'category': _('Select the category that best matches your product')
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': _('Place your bid here')
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': _('Type your comment here')
        }

@login_required(login_url='/login')
def index(request):
    category_id = request.GET.get("category", None)
    if category_id is None:
        active_listings = Listing.objects.filter(sold=False)
    else:
        active_listings = Listing.objects.filter(sold=False, category=category_id)
    return render(request, "auctions/index.html", {
        'listings': active_listings
    })

@login_required(login_url='/login')
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            NewListing = form.save(commit=False)
            NewListing.seller = request.user
            NewListing.save()

            return render(request, "auctions/create.html", {
                "form": ListingForm(),
                "success": True
            })
        
        else:
            return render(request, "auctions/create.html", {
                "form": ListingForm(),
                "error": True
            })

    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })

@login_required(login_url='/login')
def listing(request, listing_id):

    if request.method == 'GET':    
        listing = Listing.objects.get(id=listing_id)
        comments = Comment.objects.filter(listing=listing_id)
        if request.user in listing.watchers.all():
            listing.watched = True
        else:
            listing.watched = False

        if listing.seller == request.user:
            creator = True
        else:
            creator = False
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
            "creator": creator,
            "comments": comments
        })

    else:
        listing_item = Listing.objects.get(id=listing_id)
        comments = Comment.objects.filter(listing=listing_id)
        if listing_item.current_bid != None:
            
            listing_item.buyer = Bid.objects.filter(listing=listing_item).last().user
            listing_item.sold = True
            listing_item.save()

            return render(request, "auctions/listing.html", {
                "listing": listing_item,
                "comments": comments"
            })
        else:
            return render(request, "auctions/listing.html", {
            "listing": listing_item,
            "bid_form": BidForm(),
            "no_bids": True,
            "comments": comments
        })

def view_all_categories(request):
    categories = Categorie.objects.exclude(title='None')
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def view_category(request, category_id):
    if category_id is None:
        active_listings = Listing.objects.filter(sold=False)
    else:
        active_listings = Listing.objects.filter(sold=False, category=category_id)

    return render(request, "auctions/index.html", {
        'listings': active_listings
    })

@login_required(login_url='/login')
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        NewComment = form.save(commit=False)
        NewComment.user = request.user
        NewComment.listing = listing
        NewComment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    

@login_required(login_url='/login')
def watchlist(request, listing_id):
    listing_item = Listing.objects.get(id=listing_id)
    if request.user in listing_item.watchers.all():
        listing_item.watchers.remove(request.user)
    else:
        listing_item.watchers.add(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

@login_required(login_url='/login')
def show_watchlist(request):
    watched_listings = request.user.watched_listings.all()
    return render(request, "auctions/watchlist.html", {
        'listings': watched_listings
    })

@login_required(login_url='/login')
def make_bid(request, listing_id):
    if request.method == 'POST':
        form = BidForm(request.POST)
        listing_item = Listing.objects.get(id=listing_id)
        if request.user == listing_item.seller:
            return render(request, "auctions/listing.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "own_item": True
                    })
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']
            if listing_item.current_bid is None:
                if bid_amount >= listing_item.starting_bid:
                    NewBid = form.save(commit=False)
                    NewBid.user = request.user
                    NewBid.listing_id = listing_id
                    NewBid.save()
                    listing_item.current_bid = bid_amount
                    listing_item.save()
                    
                    return render(request, "auctions/listing.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "succes": True
                    })

                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "error": True
                    })
            else:
                if bid_amount > listing_item.current_bid:
                    NewBid = form.save(commit=False)
                    NewBid.user = request.user
                    NewBid.listing_id = listing_id
                    NewBid.save()
                    listing_item.current_bid = bid_amount
                    listing_item.save()
                    
                    return render(request, "auctions/listing.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "succes": True
                    })
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "error": True
                    })
        else:
            return render(request, "auctions/listing.html", {
                    "listing": listing_item,
                    "bid_form": BidForm(),
                    "error": True
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
