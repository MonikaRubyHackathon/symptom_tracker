from django.urls import path
from .views.deck_views import Decks, DeckDetail
from .views.card_views import Cards
from .views.card_views import CardDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('decks/', Decks.as_view(), name='decks'),
    path('decks/<int:pk>/', DeckDetail.as_view(), name='deck_detail'),
    path('cards/', Cards.as_view(), name='cards'),
    path('cards/<int:pk>', CardDetail.as_view(), name='card_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
