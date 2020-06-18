from rest_framework.throttling import UserRateThrottle


class UserMinuteThrottle(UserRateThrottle):
    scope = 'user_min'


class EmailMinuteThrottle(UserRateThrottle):
    scope = 'anon_min'
