from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import APIException


class UserMinuteThrottle(UserRateThrottle):
    scope = 'user_min'


class EmailMinuteThrottle(UserRateThrottle):
    scope = 'anon_min'
