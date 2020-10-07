from django.urls import path
from .views.tracker_views import Tracker
# from .views.card_views import Cards
from .views.tracker_views import TrackerDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('trackers/', Tracker.as_view(), name='trackers'),
    path('trackers/<int:pk>/', TrackerDetail.as_view(), name='tracker_detail'),
    # path('cards/', Cards.as_view(), name='cards'),
    # path('cards/<int:pk>', CardDetail.as_view(), name='card_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
