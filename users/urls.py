from django.urls import path
from users.views import KakaoLoginView, UserPointView

urlpatterns = [
    path('/login', KakaoLoginView.as_view()),
    path('/point', UserPointView.as_view()),
]