from django.urls import path

from biddings.views import BiddingView, NewBiddingView

urlpatterns = [
    path('', BiddingView.as_view()),
    path('/bidding', NewBiddingView.as_view()),
]