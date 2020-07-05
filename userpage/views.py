from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Profile, Bracelet, InfoBlock
from .serializers import *

User = get_user_model()


@permission_classes([IsAuthenticated])
class CreateProfile(APIView):
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.pk
        newProfile = ProfileCreateSerializer(data=data)
        if newProfile.is_valid():
            if Profile.objects.filter(user__id=request.user.pk).count() < settings.MAX_PROFILES_PER_USER:
                p = newProfile.save()
                return Response({"profile_id": p.id}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ViewProfile(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            profiles = Profile.objects.select_related('user').filter(user__id=user_id).order_by('id')
            serializer = ProfileViewListSerializer(profiles, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockCreateView(APIView):
    def post(self, request, profile_pk):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        status_code = status.HTTP_201_CREATED

        if (
                infoblock.is_valid() and
                InfoBlock.objects.filter(
                    profile__id=profile_pk
                ).count() < settings.MAX_INFOBLOCKS_PER_PROFILE
        ):
            try:
                profile = Profile.objects.get(pk=profile_pk)
                if profile.user == request.user:
                    block_id = infoblock.save(profile=profile).id
                    return Response({'block_id': block_id}, status=status_code)
                else:
                    status_code = status.HTTP_403_FORBIDDEN
            except ObjectDoesNotExist:
                status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(status=status_code)


@permission_classes([IsAuthenticated])
class InfoBlockDeleteView(APIView):
    def delete(self, request, profile_pk, block_pk):
        try:
            infoblock = InfoBlock.objects.get(pk=block_pk)
            profile = Profile.objects.get(pk=profile_pk)
            if infoblock.profile != profile:
                raise ObjectDoesNotExist
            if request.user == profile.user:
                infoblock.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockChangeView(APIView):
    def put(self, request, profile_pk, block_pk):
        infoblock_ser = InfoBlockCreateSerializer(data=request.data)
        if infoblock_ser.is_valid():
            try:
                infoblock = InfoBlock.objects.get(pk=block_pk)
                profile = Profile.objects.get(pk=profile_pk)

                if infoblock.profile != profile:
                    raise ObjectDoesNotExist
                if request.user == profile.user:
                    infoblock.title = infoblock_ser.validated_data['title']
                    infoblock.content = infoblock_ser.validated_data['content']
                    infoblock.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticatedOrReadOnly])
class InfoBlockFromProfileListView(APIView):
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)

            if profile.is_activated or profile.user == request.user:
                infoblocks = InfoBlock.objects.select_related('profile').filter(profile=profile).order_by('id')
                serializer = InfoBlockDetailSerializer(infoblocks, many=True)
                response_data = {
                    'name': profile.name,
                    'is_owner': profile.user == request.user,
                    'blocks': serializer.data
                }
                return Response(response_data)
            else:
                return Response(data={'status': 'Профиль не активирован'}, status=status.HTTP_423_LOCKED)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        status_code = status.HTTP_200_OK
        try:
            profile = Profile.objects.get(pk=pk)
            if request.user == profile.user:
                profile.delete()
            else:
                status_code = status.HTTP_403_FORBIDDEN
        except ObjectDoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)

    def put(self, request, pk):
        try:
            new_profile_name = NewProfileNameSerializer(data=request.data)
            if new_profile_name.is_valid():
                try:
                    profile = Profile.objects.get(pk=pk)
                    if request.user == profile.user:
                        profile.name = new_profile_name.validated_data['name']
                        profile.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_403_FORBIDDEN)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class BraceletFromProfile(APIView):
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            if request.user == profile.user and profile.is_activated:
                bracelets = Bracelet.objects.select_related('profile').filter(profile=profile).order_by('id')
                serializer = BraceletsFromProfileSerializer(bracelets, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'status': 'Браслеты или профиль не найдены'}, status=status.HTTP_423_LOCKED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class AccountDefinition(APIView):
    def get(self, request, pk):
        try:
            bracelet = Bracelet.objects.get(id=pk)
            if bracelet.profile:
                data = {
                    'profile_id': bracelet.profile_id,
                }
                return Response(data=data)
            else:
                return Response({'status': 'bracelet is not attached'}, status=status.HTTP_423_LOCKED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class JoinHandler(APIView):
    def post(self, request, pk):
        try:
            unique_code = request.data['unique_code']
            profile_id = int(request.data['profile_id'])

            bracelet = Bracelet.objects.get(pk=pk)
            profile = Profile.objects.get(pk=profile_id)

            if bracelet.profile:
                return Response({"status": "Bracelet already activated"}, status=status.HTTP_400_BAD_REQUEST)

            if request.user == profile.user and bracelet.unique_code == unique_code:
                bracelet.profile = profile
                profile.is_activated = True
                bracelet.save()
                profile.save()
                return Response({"status": "Attached to profile"})
            else:
                return Response({"status": "Invalid unique_code or profile_id"}, status=status.HTTP_400_BAD_REQUEST)

        except (KeyError, ValueError, TypeError):
            return Response({"status": "unique_code and profile_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": "no such bracelet or profile"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            profile_id = int(request.data['profile_id'])
            bracelet = Bracelet.objects.get(pk=pk)
            if bracelet.profile.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            old_profile = bracelet.profile
            profile = Profile.objects.get(pk=profile_id)

            if request.user == profile.user:
                bracelet.profile = profile
                profile.is_activated = True
                bracelet.save()
                profile.save()
                if Bracelet.objects.select_related('profile').filter(profile__id=old_profile.id).count() <= 0:
                    old_profile.is_activated = False
                    old_profile.save()
                return Response({"status": "Attached to profile"})
            else:
                return Response({"status": "Invalid unique_code or profile_id"}, status=status.HTTP_400_BAD_REQUEST)

        except (KeyError, ValueError, TypeError):
            return Response({"status": "unique_code and profile_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": "no such bracelet or profile"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_unique_valid(request, pk):
    try:
        bracelet = Bracelet.objects.get(id=pk)
        if bracelet.unique_code == request.data.get('unique_code'):
            data = {"is_valid": True}
        else:
            data = {"is_valid": False}
        return Response(data=data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class DisconnectBracelet(APIView):
    def post(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)

            if request.user != profile.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            bracelet = Bracelet.objects.get(profile__id=pk, id=request.data['id'])
            bracelet.profile = None
            bracelet.save()
            if Bracelet.objects.select_related('profile').filter(profile__id=profile.id).count() <= 0:
                profile.is_activated = False
                profile.save()
            return Response({"status": "Bracelet disconnected"})

        except (KeyError, ValueError, TypeError):
            return Response({"status": "unique_code and profile_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": "no such bracelet or profile"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAdminUser])
class createhandler(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=403)

        handler = CreateBraceletSerializer(data=request.data)
        if handler.is_valid():
            b = handler.save()
            return Response({'bracelet_id': b.id}, status=201)
        else:
            return Response(handler.errors, status=400)


@permission_classes([IsAdminUser])
class CreateManyHandlers(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=403)
        try:
            amount = int(request.data.get('amount'))

            import random
            import string
            bracelets = []
            success = 0

            for i in range(amount):
                generated_code = ''.join(
                    random.SystemRandom().choice(string.ascii_lowercase + string.digits)
                    for _ in range(8)
                )
                try:
                    Bracelet.objects.get(unique_code=generated_code)
                except ObjectDoesNotExist:
                    b = Bracelet.objects.create(unique_code=generated_code)
                    b.save()
                    bracelets.append({"bracelet_id": b.id, "unique_code": generated_code})
                    success += 1

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({'saved_bracelets_amount': success, 'bracelets': bracelets}, status=status.HTTP_201_CREATED)


@permission_classes([IsAdminUser])
class deleteHandler(APIView):
    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response(status=403)
        try:
            handler = Bracelet.objects.get(pk=pk)
            handler.delete()
            return Response(status=200)
        except:
            return Response(status=404)
