import json, jwt

from django.test     import TestCase, Client

from biddings.models import Bidding
from products.models import Product, ProductSize, Size, Brand
from users.models    import User
from my_settings     import SECRET_KEY, ALGORITHM

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

class NewBiddingViewUnitTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = 1
        )

        Brand.objects.create(
            id   = 1,
            name = "Nike"
        )

        Size.objects.create(
            id   = 1,
            name = '260'
        )

        Product.objects.create(
            id            = 1,
            name          = "Nike Dunk Low Retro Black",
            korean_name   = "나이키 덩크 로우 레트로 블랙",
            model_number  = "DD1391-100",
            color         = "WHITE/BLACK",
            release_at    = "2021-01-14",
            retail_price  = 129000,
            thumbnail_url = 'https://testimgurl.com',
            brand_id      = 1
        )

        ProductSize.objects.create(
            id         = 1,
            product_id = 1,
            size_id    = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()

    def test_newbiddingview_post_filtering(self):
        client = Client()

        access_token      = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)
        headers           = {'HTTP_AUTHORIZATION': access_token}

        data = {
            'is_buyer'      : False,
            'offered_price' : 11111,
            'id'            : 1,
            'size'          : 'wrong'
        }
        response = client.post('/biddings/bidding', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 204)

    def test_newbiddingview_post_success(self):
        client = Client()

        access_token      = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)
        headers           = {'HTTP_AUTHORIZATION': access_token}

        data = {
            'user'          : 1,
            'is_buyer'      : 0,
            'offered_price' : 11111,
            'id'            : 1,
            'size'          : '260'
        }
        response = client.post('/biddings/bidding', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'OFFER_SUCCESS'})

    def test_newbiddingview_post_keyerror(self):
        client = Client()

        access_token      = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)
        headers           = {'HTTP_AUTHORIZATION': access_token}

        data = {
            'is_buyer'      : False,
            'offered_price' : 11111,
            'wrong_id'      : 1,
            'size'          : '260'
        }
        response = client.post('/biddings/bidding', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})