from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listingID>/", views.view_listing, name="view_listing"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("bid/<int:status>", views.bid, name="bid"),
    path("close", views.close, name="close")
]
