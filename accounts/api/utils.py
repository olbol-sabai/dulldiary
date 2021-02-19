# from django.conf import settings
# from django.utils import timezone
# import datetime



# time_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
# now = timezone.now()

# def jwt_response_payload_handler(token, user=None):
#     username = 'undefined'
#     if user is not None:
#         username = user.username
#     return {
#         'token': token,
#         'user': username,
#         'token_refresh_expires_at': now + time_delta - datetime.timedelta(seconds=200)
#     }
