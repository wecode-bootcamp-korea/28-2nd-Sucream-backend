from django.urls import path

from products.views import ProductListView, FilterBarView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/filter', FilterBarView.as_view()),
    
]
