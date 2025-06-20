"""
Use UntypedToken to validate the signature and expiry
=============================
jwt.decode() with SECRET_KEY and ALGORITHM from our SIMPLE_JWT settings to extract user
=============================
get_user() fetches the real Django user
"""


import logging, traceback
from urllib.parse import parse_qs
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger("communications")

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    pk_name = User._meta.pk.name
    try:
        return User.objects.get(**{pk_name: user_id})
    except User.DoesNotExist:
        return AnonymousUser()
    
class JwtAuthMiddleware:
    """
    Extracts a JWT access token from ?token=<token> and
    populates scope['user'] if valid, or AnonymousUser
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            qs = parse_qs(scope.get("query_string", b"").decode())
            token = qs.get("token", [None])[0]

            user = AnonymousUser()

            if token:
                UntypedToken(token)
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
                    options={"verify_exp": True},
                )
                user = await get_user(payload[settings.SIMPLE_JWT["USER_ID_CLAIM"]])

            scope["user"] = user
            return await self.app(scope, receive, send)
        
        except (InvalidToken, TokenError, jwt.PyJWTError) as e:
            logger.warning(f"JWT authorization failed: {e}")
            scope["user"] = AnonymousUser() 
            return await self.app(scope, receive, send)
        
        except Exception as e:
            logger.error(f"Error in JwtAuthMiddleWare: {e}\n {traceback.format_exc()}")
            raise