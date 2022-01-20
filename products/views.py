from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Min, Max

from products.models import Product, Brand, Size
from biddings.models import Order

class ProductListView(View):
    def get(self, request):
        brands   = request.GET.getlist('brand', None)
        sizes    = request.GET.get('size', None)
        order    = request.GET.get('order', 'recent')
        is_buyer = request.GET.get('is_buyer', 1)

        filtering = Q()

        if brands:
            filtering &= Q(brand__id__in = brands)

        if sizes:
            size_list  = sizes.split(',')
            filtering &= Q(sizes__id__in = size_list)

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

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXISTS'}, status=404)

        product = Product.objects.get(id=product_id)

        images     = product.image_set.all()
        image_urls = [image.url for image in images]
        image_urls.insert(0,product.thumbnail_url)

        like_count = product.like_set.filter(is_like=True).count()

        result = {
            'product_id'   : product.id,
            'brand'        : product.brand.name,
            'name'         : product.name,
            'korean_name'  : product.korean_name,
            'model_number' : product.model_number,
            'color'        : product.color,
            'release_at'   : product.release_at,
            'retail_price' : int(product.retail_price),
            'image_urls'   : image_urls,
            'like_count'   : like_count,
            'is_like'      : False
        }
        return JsonResponse({'result' : result}, status = 200)

class ProductDetailGraphView(View):
    def get(self, request, product_id):
        try:
            result = [{
                'id'         : order.id,
                'size'       : order.products_sizes.size.name,
                'price'      : int(order.price),
                'created_at' : order.created_at.strftime('%Y/%m/%d')
            } for order in Order.objects.filter(products_sizes__product_id=product_id).order_by('-created_at')]

            return JsonResponse({'result' : result}, status = 200)

        except Order.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ORDER'}, status=401)