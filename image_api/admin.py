from django.contrib import admin

from .models import Image, ImageSize, ImageContainer, ImageLink, Tier, UserTier


class TierAdmin(admin.ModelAdmin):
    list_display = ["name", "originalLink", "expiringLink"]

class UserTierAdmin(admin.ModelAdmin):
    list_display = ["user", "tier"]

class ImageSizesAdmin(admin.ModelAdmin):
    list_display = ["tier", "height"]

class ImageLinkAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "link", "expiration_time", "created_time"]

admin.site.register(UserTier, UserTierAdmin)
admin.site.register(ImageSize, ImageSizesAdmin)
admin.site.register(ImageLink, ImageLinkAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(Image)





