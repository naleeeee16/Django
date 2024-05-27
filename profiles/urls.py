from django.urls import path, include
from profiles import views as profiles_view

urlpatterns = [
    path("profile_info", profiles_view.view_profile_info, name="profile_info"),
    path("profile_collection", profiles_view.view_profile_collection, name="profile_collection"),
    path("profile_portfolio", profiles_view.view_profile_portfolio, name="profile_portfolio"),
    path("profile_exhibitions", profiles_view.view_profile_exhibitions, name="profile_exhibitions"),
    path("collection_sort",profiles_view.sort_profile_collection,name = "collection_sort"),
    path("portfolio_sort",profiles_view.sort_profile_collection,name = "portfolio_sort"),
    path("exhibition_sort",profiles_view.sort_profile_exhibition,name = "exhibition_sort"),
    path("change_info", profiles_view.view_change_info, name="change_info"),
   path("change_info_submit", profiles_view.change_info, name="submit_change_info")


]
