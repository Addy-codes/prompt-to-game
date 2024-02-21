from django.contrib import admin
from game.models import Game, Image_Assets, Sound_Asset
# Register your models here.

admin.site.register(Game)
admin.site.register(Image_Assets)
admin.site.register(Sound_Asset)