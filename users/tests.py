import json, requests, jwt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
			kakao_id = 123456789,
            email    = '123456789@gmail.com',
            point    = 10000000
        )
    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakaologinview_get_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":123456789,
                    "kakao_account": {
                        "email" : "123456789@gmail.com"
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "3242343242343234"}
        response            = client.get("/users/login", **headers)
        access_token        = jwt.encode({'user_id': 1}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'access_token': access_token})

    @patch("users.views.requests")
    def test_kakaologinview_get_keyerror(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "wrong_id":123456789,
                    "kakao_account": {
                        "email" : "123456789@gmail.com"
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "3242343242343234"}
        response            = client.get("/users/login", **headers)

        self.assertEqual(response.status_code, 400)