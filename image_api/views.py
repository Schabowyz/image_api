from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Image, ImageContainer, ImageLink, ImageSize, UserTier, Tier
from .serializers import UserSerializer, ImageContainerSerializer


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
    return Response({"user": request.user.username, "images": serializer.data})


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
    return Response({"image": serializer.data})


def render_image(request, image_link):
    image = get_object_or_404(ImageLink, link=image_link).image.image
    return HttpResponse(image, content_type="image/png")


