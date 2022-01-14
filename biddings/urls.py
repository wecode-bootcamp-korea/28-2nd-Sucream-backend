from django.urls import path

from biddings.views import BiddingView

urlpatterns = [
    path('', BiddingView.as_view()),
]