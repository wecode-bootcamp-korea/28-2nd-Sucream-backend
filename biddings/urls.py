from django.urls import path

from biddings.views import BiddingView, NewBiddingView, OrderView

urlpatterns = [
    path('', BiddingView.as_view()),
    path('/order', OrderView.as_view()),
    path('/bidding', NewBiddingView.as_view()),
]