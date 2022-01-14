from django.test import TestCase, Client

from biddings.models import Bidding
from products.models import Product, ProductSize, Size, Brand
from users.models import User

class BiddingUnitTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 1234,
            email    = "gusrn015@gmail.com"
        )
        Size.objects.create(
            id   = 1,
            name = "230"
        )
        Brand.objects.create(
            id   = 1,
            name = "Nike"
        )
        Product.objects.create(
            id            = 1,
            name          = "Nike Dunk Black",
            korean_name   = "나이키 덩크 블랙",
            model_number  = "DD1391-100",
            color         = "WHITE/BLACK",
            release_at    = "2021-01-14",
            retail_price  = "129000",
            thumbnail_url = "url",
            brand_id      = 1,
        )
        ProductSize.objects.create(
            id         = 1,
            product_id = 1,
            size_id    = 1
        )
        Bidding.objects.create(
            id                = 1,
            price             = 1000,
            is_buyer          = True,
            user_id           = 1,
            products_sizes_id = 1
        )
        Bidding.objects.create(
            id                = 2,
            price             = 2000,
            is_buyer          = False,
            user_id           = 1,
            products_sizes_id = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Size.objects.all().delete()
        Brand.objects.all().delete()
        Product.objects.all().delete()
        ProductSize.objects.all().delete()
        Bidding.objects.all().delete()

    def test_bidding_get_success(self):
        client = Client()
        response = client.get('/biddings?product=1')

        result = {
                "instant_buy"  : 1000,
                "instant_sell" : 2000,
                "buy"          : [{
                    "id"    : 1,
                    "size"  : "230",
                    "price" : 1000
                }],
                "sell"         : [{
                    "id"    : 1,
                    "size"  : "230",
                    "price" : 2000
                }],
            }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})

    def test_bidding_get_product_required(self):
        client = Client()
        response = client.get('/biddings')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "PRODUCT_REQUIRED"})

    def test_bidding_get_product_does_not_exist(self):
        client = Client()
        response = client.get('/biddings?product=300')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "PRODUCT_DOES_NOT_EXIST"})