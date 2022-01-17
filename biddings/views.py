import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Max, Min

from products.models import Product, Size, ProductSize
from biddings.models import Order, Bidding
from users.models    import User
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

class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            product  = data['product']
            size     = data['size']
            price    = str(data['price'])
            is_buyer = data['is_buyer']
            is_buyer = bool(is_buyer)

            if not ProductSize.objects.filter(size__name = size, product_id = product).exists():
                return JsonResponse({"message" :  "product_size does not exist"}, status=204)
                
            product_size = ProductSize.objects.get(product_id = product, size__name = size).id
            bidding      = Bidding.objects.filter(products_sizes_id = product_size, price = price).exclude(is_buyer = is_buyer).first()
            price        = int(bidding.price)

            if is_buyer:
                buy_user_id  = user.id
                sell_user_id = bidding.user_id
            else:
                buy_user_id  = bidding.user_id
                sell_user_id = user.id

            buy_user  = User.objects.get(id=buy_user_id)
            sell_user = User.objects.get(id=sell_user_id)

            buy_user_point  = int(buy_user.point)
            sell_user_point = int(sell_user.point)

            if buy_user_point < price:
                return JsonResponse({"message" : "NOT_ENOUGH_POINT"}, status = 400)

            Order.objects.create(
                buyer_id          = buy_user_id,
                seller_id         = sell_user_id,
                price             = price,
                products_sizes_id = product_size,
                status_id         = 1
            )
        
            buy_user.point = buy_user_point - price
            sell_user.point = sell_user_point + price

            buy_user.save()
            sell_user.save()
            bidding.delete()

            return JsonResponse({"message" : "success"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except ValueError:
            return JsonResponse({"message" : "BIDDING_DOES_NOT_EXIST"}, status = 400)