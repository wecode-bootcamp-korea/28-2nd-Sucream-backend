import json
import jwt

from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def login_decorator():
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        return func(self, request,  *args, **kwargs)