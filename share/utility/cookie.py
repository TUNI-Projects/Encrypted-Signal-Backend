from decouple import config
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings

def cookie_monster(response: JsonResponse, key: str, val: str):
    expires = datetime.now() + timedelta(hours=12)
    IS_DEBUG = settings.DEBUG

    if IS_DEBUG:
        response.set_cookie(key, val,
                            domain='',
                            path='/',
                            expires=expires,
                            secure=False,
                            samesite='Strict')
    else:
        response.set_cookie(key, val,
                            domain='',
                            path='/',
                            expires=expires,
                            secure=True,
                            samesite='None')
    return response
