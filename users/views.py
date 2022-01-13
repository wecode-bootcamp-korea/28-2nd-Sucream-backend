import requests, jwt

from django.http.response import JsonResponse
from django.conf          import settings
from django.views         import View

from my_settings       import SECRET_KEY, ALGORITHM
from users.models      import User

class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token   = request.headers['Authorization']
            kakao_account = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {kakao_token}'}).json()

            if not User.objects.filter(kakao_id=kakao_account['id']).exists():
                user = User.objects.create(
                    kakao_id = kakao_account['id'],
                    email    = kakao_account['kakao_account']['email']
                )
            else:
                user = User.objects.get(kakao_id=kakao_account['id'])

            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'access_token': access_token}, status=201)

        except KeyError:
            return JsonResponse({'message': 'AUTHORIZATION_KEY_ERROR'}, status=400)