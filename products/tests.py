from django.test import TestCase, Client

from products.models import Product, Brand, Size, ProductSize
from biddings.models import Order, Status
from users.models    import User

class ProductDetailTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id       = 1,
                kakao_id = 1
            ),
            User(
                id       = 2,
                kakao_id = 2
            )
        ])
        Brand.objects.create(
            id   = 1,
            name = "Nike"
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
        Size.objects.create(
            id   = 1,
            name = '260'
        )
        ProductSize.objects.create(
            id = 1,
            product_id =1,
            size_id = 1
        )
        Status.objects.create(
            id   = 1,
            name = '주문완료'
        )
        Order.objects.create(
            id                = 1,
            buyer_id          = 2,
            seller_id         = 1,
            price             = 10000,
            products_sizes_id = 1,
            status_id         = 1
        )
    def tearDown(self):
        User.objects.all().delete()
        Brand.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Status.objects.all().delete()
        Order.objects.all().delete()

    def test_productdetailview_get_success(self):
        client = Client()
        response = client.get('/products/1')

        self.assertEqual(response.status_code, 200)
    def test_productdetailview_get_error(self):
        client = Client()
        response = client.get('/products/2')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'PRODUCT_DOES_NOT_EXISTS'})

    def test_productdetailgraphview_get_success(self):
        client   = Client()
        response = client.get('/products/1/graph')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'result' : [{
                    'id'         : 1,
                    'size'       : '260',
                    'price'      : 10000,
                    'created_at' : '2022/01/20'#오늘날짜로 직접 입력필요
                }]
            }
        )
