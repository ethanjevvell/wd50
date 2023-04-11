from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Listing, Bid, User, Comment
from .forms import NewListingForm

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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


def view_listing(request, listingID):

    listing = Listing.objects.filter(pk=listingID).first()
    comments = Comment.objects.filter(listing=listingID)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def comment(request):
    if request.method == "POST":
        commentUser = request.user
        commentBody = request.POST["comment_body"]
        listingID = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listingID)
        newComment = Comment(user=commentUser, commentBody=commentBody, listing=listing)
        newComment.save()

    return redirect("index")


def bid(request, status):

    if request.method == "POST":
        bid_amount = int(request.POST["bid_amount"])
        listing_id = request.POST["listing_id"]

        try:
            listing_highest_bid = Bid.objects.filter(listingID=listing_id).order_by("-bidAmount").first()["bidAmount"]
        except:
            listing_highest_bid = Listing.objects.filter(pk=listing_id).values("startingBid").first()["startingBid"]

        user = request.user

        if not bid_amount > listing_highest_bid:
            return render(request, "auctions/bid.html", {
                "status": 0
            }) #TODO: Error for not bidding high enough

        listing = Listing.objects.get(pk=listing_id)

        bid = Bid(user=user, listingID=listing, bidAmount=bid_amount, postedTime=timezone.now())
        bid.save()

        listing.startingBid = bid_amount
        listing.save()

        return render(request, "auctions/bid.html", {
            "status": 1
        })


def close(request):

    listing_id = int(request.POST["listing_id"])
    listing = Listing.objects.get(pk=listing_id)
    winner = Bid.objects.filter(listingID=listing_id).order_by("-bidAmount").first().user
    listing.winner = winner
    listing.save()

    return render(request, "auctions/close.html")

@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        listingID = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listingID)

        if listing not in request.user.watchlist.all():
            request.user.watchlist.add(listing)
        else:
            request.user.watchlist.remove(listing)

        return redirect("view_listing", listingID=listingID)

    else:
        return redirect("index")

@login_required
def new_listing(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            # Collect form data
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            startingBid = form.cleaned_data["startingBid"]
            description = form.cleaned_data["description"]
            imageURL = form.cleaned_data["imageURL"]

            # Create instance of Listing model; save to db
            listing = Listing(title=title, category=category, startingBid=startingBid, description=description, imageURL=imageURL, creator=request.user, winner=None)
            listing.save()

    else:
        form = NewListingForm()

    return render(request, "auctions/new_listing.html", {"form": form})