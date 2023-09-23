from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image as PilImage

import os
from uuid import uuid4


##### FUNCTIONS #####

def path_and_rename(self, filename):
    upload_to = "images"
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)

def generate_link():
    return f"{uuid4().hex}"



##### MODELS #####

class Tier(models.Model):
    name = models.TextField(max_length=64, null=False)
    originalLink = models.BooleanField(null=False, default=False)
    expiringLink = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name
    

class UserTier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)


class ImageSize(models.Model):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    height = models.IntegerField()

    def __str__(self):
        return self.tier.name
    

class ImageContainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_images_and_links(self, image_file):
        og_image = Image(
            container = self,
            image = image_file
        )
        og_image.save()
        og_link = ImageLink(
            image = og_image,
        )
        og_link.save()

        possible_heights = ImageSize.objects.filter(tier=UserTier.objects.get(user=self.user).tier)
        for height in possible_heights:
            new_image = Image(
                container = self,
                original = False,
                image = image_file
            )
            new_image.save()

            resize = PilImage.open(new_image.image)
            resize.thumbnail((resize.width, height.height))
            resize.save(new_image.image.path)
            
            new_link = ImageLink(
                image = new_image,
                height = height
            )
            new_link.save()

    @property
    def images_urls(self):
        urls = {}
        images = Image.objects.filter(container=self)
        for image in images:
            link = ImageLink.objects.get(image=image)
            if link.height:
                urls[link.height.height] = f"/share/{link.link}"
            else:
                urls["original"] = f"/share/{link.link}"
        return urls


class Image(models.Model):
    container = models.ForeignKey(ImageContainer, on_delete=models.CASCADE)
    original = models.BooleanField(default=True)
    image = models.ImageField(upload_to=path_and_rename)


class ImageLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    height = models.ForeignKey(ImageSize, on_delete=models.CASCADE, null=True)
    link = models.CharField(null=False, default=generate_link, max_length=128)
    expiration_time = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=now, editable=False)