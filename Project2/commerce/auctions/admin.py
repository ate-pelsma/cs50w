from django.contrib import admin
from auctions.models import Categorie, User, Listing, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Categorie)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)