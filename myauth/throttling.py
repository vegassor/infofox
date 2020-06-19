from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import APIException


class EmailMinuteThrottle(UserRateThrottle):
    scope = 'anon_min'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service unavailable, try again later.'
    default_code = 'service_unavailable'
