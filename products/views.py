from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Min, Max

from products.models import Product, Brand, Size

class ProductListView(View):
    def get(self, request):
        brands   = request.GET.getlist('brand', None)
        sizes    = request.GET.getlist('size', None)
        order    = request.GET.get('order', 'recent')
        is_buyer = request.GET.get('is_buyer', 1)

        is_buyer = bool(int(is_buyer))

        filtering = Q()

        if brands:
            filtering &= Q(brand__id__in = brands)

        if sizes:
            filtering &= Q(sizes__id__in = sizes)

        if is_buyer:
            filtering &= Q(productsize__bidding__is_buyer = True)
            products   = Product.objects\
                                .annotate(price=Min("productsize__bidding__price"))\
                                .filter(filtering)

        if not is_buyer:
            filtering &= Q(productsize__bidding__is_buyer = False)
            products   = Product.objects\
                                .annotate(price=Max("productsize__bidding__price"))\
                                .filter(filtering)

        ordering_field = {
            "recent"     : "-release_at",
            "low_price"  : "price",
            "high_price" : "-price"
        }
        
        ordering = ordering_field.get(order, "-release_at")

        result = [{
                "id"            : product.id,
                "brand"         : product.brand.name,
                "name"          : product.name,
                "korean_name"   : product.korean_name,
                "price"         : int(product.price),
                "thumbnail_url" : product.thumbnail_url
            } for product in products.order_by(ordering)]

        return JsonResponse({"result" : result}, status=200)

class FilterBarView(View):
    def get(self, request):
        brands = Brand.objects.all()
        sizes  = Size.objects.all()

        result = {
            "brand" : [
                {
                    "id"   : brand.id,
                    "name" : brand.name
                } for brand in brands],
            "size"  : [
                {
                    "id"   : size.id, 
                    "name" : size.name
                } for size in sizes]
            }

        return JsonResponse({"result" : result}, status=200)