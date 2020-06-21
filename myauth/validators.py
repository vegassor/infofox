from django.core.exceptions import ValidationError


def validate_purpose(value):
    if value not in {'question', 'offer', 'jobResponse', 'comment', 'claim'}:
        raise ValidationError(
            "the value should be one of: 'question', 'offer', 'jobResponse', 'comment', 'claim'"
        )


def not_empty(value):
    if value == '':
        raise ValidationError(
            'Это поле не может быть пустым'
        )

# class UniqueOrBlankEmailValidator:
#     def __init__(self):
#         pass
#
#     def __call__(self, value):
#         try:
#             print('worked')
#             email = User.objects().get(email=value)
#             if email != '':
#                 raise ValidationError
#         except ObjectDoesNotExist:
#             pass
