from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAdminUser])
def is_admin(request, *args, **kwargs):
    return Response(data={"User_is_admin": True}, status=status.HTTP_200_OK)
