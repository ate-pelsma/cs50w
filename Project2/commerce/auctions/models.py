from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT, PROTECT
from django.utils import timezone

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

    def __str__(self):
        return f"{self.username}"

class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    starting_bid = models.DecimalField(max_digits=19, decimal_places=2)
    current_bid = models.DecimalField(blank=True, null=True, max_digits=19, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(Categorie, blank=True, default=8, on_delete=models.CASCADE, related_name="categorie_listings")
    image = models.TextField(blank=True)
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing}: {self.amount} by {self.user}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(default=timezone.now)


