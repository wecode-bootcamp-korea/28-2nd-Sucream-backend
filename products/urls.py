from django.urls import path

from products.views import ProductListView, FilterBarView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/filter', FilterBarView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]