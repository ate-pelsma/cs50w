from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.show_watchlist, name="show_watchlist"),
    path("listing/<int:listing_id>/bid", views.make_bid, name="make_bid"),
    path("categories", views.view_all_categories, name="all_categories"),
    path("categories/<int:category_id>", views.view_category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
