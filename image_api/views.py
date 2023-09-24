from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

import datetime

from .models import ImageContainer, ImageLink, UserTier
from .serializers import UserSerializer, ImageContainerSerializer


@api_view(["GET"])
def index(reqeust):
    return Response({
        "login - for auth token generation": "/login",
        "user's images (requires auth token)": "/images",
        "image upload (requires auth token)": "/upload"
    })


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found"}, stauts=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_images(request):
    image_containers = ImageContainer.objects.filter(user=request.user)
    serializer = ImageContainerSerializer(image_containers, many = True, context = {"user": request.user.id})
    return Response({"user": request.user.username,
                     "info": "to generate expiring link, use one of original links and add '/TIMEINSECONDS' after. Value must be between 300 and 30000",
                     "images": serializer.data})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_image(request):
    try:
        image_container = ImageContainer(
            user = request.user
        )
        image_container.save()
        image_container.save_images_and_links(request.data["image"])
    except:
        return Response("Image not provided")
    serializer = ImageContainerSerializer(instance=image_container)
    return Response({"info": "to generate expiring link, use one of original links and add '/TIMEINSECONDS' after. Value must be between 300 and 30000",
                     "image": serializer.data})


# Checks wether link is permament or temporary and deletes it if its outdated
def render_image(request, image_link):
    link = get_object_or_404(ImageLink, link=image_link)
    if link.expiration_time != 0:
        created_time = link.created_time.replace(tzinfo=None)
        timediff = datetime.datetime.now() - created_time
        if timediff.total_seconds() > link.expiration_time:
            link.delete_outdated_link()
            return JsonResponse({"404": "outdated link"}, status=404)
    return HttpResponse(link.image.image, content_type="image/png")


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_expiring_link(request, image_link, expiration_time_seconds):

    if UserTier.objects.get(user=request.user).tier.expiringLink == False:
        return Response({"error": "insufficent rights, please upgrade account tier to do that"})

    if int(expiration_time_seconds) < 300 or int(expiration_time_seconds) > 30000:
        return Response({"error": "expiration time must be between 300 and 30000 seconds"})

    expiring_link = ImageLink.generate_expiring_link(image_link, expiration_time_seconds)

    image_container = expiring_link.image.container
    serializer = ImageContainerSerializer(instance=image_container)
    return Response({"image": serializer.data})