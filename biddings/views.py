import json, jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Max, Min

from products.models import Product, Size, ProductSize
from users.models    import User
from biddings.models import Bidding
from cores.utils     import login_decorator

class BiddingView(View):
    def get(self, request):
        product_id = request.GET.get("product", None)

        if not product_id:
            return JsonResponse({"message" : "PRODUCT_REQUIRED"}, status = 400)

        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)

        buy_products  = ProductSize.objects\
                                    .annotate(price=Min("bidding__price"))\
                                    .filter(product_id = product_id)
        sell_products = ProductSize.objects\
                                    .annotate(price=Max("bidding__price"))\
                                    .filter(product_id = product_id)

        instant_buy  = min([int(product.price) for product in buy_products if product.price])
        instant_sell = max([int(product.price) for product in sell_products if product.price])

        result = {
            "instant_buy"  : instant_buy,
            "instant_sell" : instant_sell,
            "buy" : [{
                "id"    : product.size.id,
                "size"  : product.size.name,
                "price" : int(product.price)
            } if product.price
            else {
                "id"    : product.size.id,
                "size"  : product.size.name,
                "price" : 0
            }
            for product in buy_products],
            "sell" : [{
                "id"    : product.size.id,
                "size"  : product.size.name,
                "price" : int(product.price)
            } if product.price
            else {
                "id"    : product.size.id,
                "size"  : product.size.name,
                "price" : 0
            }for product in sell_products],
        }

        return JsonResponse({"result" : result}, status=200)

class NewBiddingView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)

            user     = request.user
            is_buyer = data['is_buyer']
            price    = data['offered_price']
            product  = data['id']
            size     = data['size']

            if not ProductSize.objects.filter(size__name = size, product_id = product).exists():
                return JsonResponse({'message' : 'PRODUCTSIZE_DOES_NOT_EXIST'}, status=204)

            product_size = ProductSize.objects.get(size__name = size, product_id = product)

            Bidding.objects.create(
                user_id           = user.id,
                is_buyer          = is_buyer,
                price             = price,
                products_sizes_id = product_size.id
            )

            return JsonResponse({'message' : 'OFFER_SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)