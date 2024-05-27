from django.urls import path, include
from nft import views as nft_views

urlpatterns = [
    path("create_nft", nft_views.create_nft, name="create_nft"),
    path("nft_review/<int:idnft>", nft_views.nft_review, name='nft_review'),
    path("nft_review/graded", nft_views.grade_nft, name='grade_nft'),
    path("change_price", nft_views.change_price, name='change_price'),
    path("buy_nft", nft_views.buy_nft, name ='buy_nft')
]