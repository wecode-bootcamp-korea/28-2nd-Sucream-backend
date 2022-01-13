from django.test import TestCase, Client

from products.models import Product, Brand, Size, ProductSize
from biddings.models import Bidding
from users.models    import User

class ProductListUnitTest(TestCase):
    def setUp(self):
        Brand.objects.create(
            id   = 1,
            name = 'Nike'
        )
        Brand.objects.create(
            id   = 2,
            name = 'Adidas'
        )
        Size.objects.create(
            id   = 1,
            name = '230'
        )
        Size.objects.create(
            id   = 2,
            name = '240'
        )
        User.objects.create(
            id       = 1,
            kakao_id = 100,
            email    = "gusrn015@gmail.com"
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
        Product.objects.create(
            id            = 2,
            name          = "Adidas SuperX",
            korean_name   = "아디다스 슈퍼 엑스",
            model_number  = "DO9391-201",
            color         = "WHITE/BLACK",
            release_at    = "2019-03-22",
            retail_price  = "185400",
            thumbnail_url = "url2",
            brand_id      = 2,
        )
        ProductSize.objects.create(
            id         = 1,
            product_id = 1,
            size_id    = 1
        )
        ProductSize.objects.create(
            id         = 2,
            product_id = 2,
            size_id    = 2
        )
        Bidding.objects.create(
            price             = 1000,
            is_buyer          = True,
            user_id           = 1,
            products_sizes_id = 1
        )
        Bidding.objects.create(
            price             = 2000,
            is_buyer          = False,
            user_id           = 1,
            products_sizes_id = 2
        )

    def tearDown(self):
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Bidding.objects.all().delete()
    
    def test_productlistview_get_success(self):
        client = Client()
        response = client.get('/products')
        
        result = [
            {
                "id"            : 1,
                "brand"         : "Nike",
                "name"          : "Nike Dunk Black",
                "korean_name"   : "나이키 덩크 블랙",
                "price"         : 1000,
                "thumbnail_url" : "url"
            },
            {
                "id"            : 2,
                "brand"         : "Adidas",
                "name"          : "Adidas SuperX",
                "korean_name"   : "아디다스 슈퍼 엑스",
                "price"         : 0,
                "thumbnail_url" : "url2"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})

    def test_productlistview_get_brand_filter_success(self):
        client = Client()
        response = client.get('/products?brand=1')
        
        result = [
            {
                "id"            : 1,
                "brand"         : "Nike",
                "name"          : "Nike Dunk Black",
                "korean_name"   : "나이키 덩크 블랙",
                "price"         : 1000,
                "thumbnail_url" : "url"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})

    def test_productlistview_get_size_filter_success(self):
        client = Client()
        response = client.get('/products?size=2')
        
        result = [
            {
                "id"            : 2,
                "brand"         : "Adidas",
                "name"          : "Adidas SuperX",
                "korean_name"   : "아디다스 슈퍼 엑스",
                "price"         : 0,
                "thumbnail_url" : "url2"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})

    def test_productlistview_get_order_success(self):
        client = Client()
        response = client.get('/products?sort=highest')
        
        result = [
            {
                "id"            : 2,
                "brand"         : "Adidas",
                "name"          : "Adidas SuperX",
                "korean_name"   : "아디다스 슈퍼 엑스",
                "price"         : 2000,
                "thumbnail_url" : "url2"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})

class FilterBarUnitTest(TestCase):
    def setUp(self):
        Brand.objects.create(
            id   = 1,
            name = 'Nike'
        )
        Brand.objects.create(
            id   = 2,
            name = 'Adidas'
        )
        Size.objects.create(
            id   = 1,
            name = '230'
        )
        Size.objects.create(
            id   = 2,
            name = '240'
        )

    def tearDown(self):
        Brand.objects.all().delete()
        Size.objects.all().delete()

    def test_filterbarview_get_success(self):
        client = Client()
        response = client.get('/products/filter')
        
        result = {
            "brand" : [
                {
                    "id"   : 1,
                    "name" : "Nike"
                },
                {
                    "id"   : 2,
                    "name" : "Adidas"
                }],
            "size" : [
                {
                    "id"   : 1,
                    "name" : "230"
                },
                {
                    "id"   : 2,
                    "name" : "240"
                }]
            }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : result})