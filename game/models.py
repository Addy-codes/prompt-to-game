from django.utils.timezone import now
from django.db import models
from user.models import CustomUser
import uuid

# Create your models here.

class Game(models.Model):
    game_name = models.CharField(max_length=255, default='default_name')
    descriptions = models.TextField(default="default_descriptions")
    search_descriptions = models.TextField(
        default='default_search_descriptions')

    def __str__(self):
        return self.game_name


class Image_Assets(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='image_asset')
    asset_name = models.CharField(max_length=255, default='default_asset_name')
    path = models.CharField(max_length=255, default='default_path')
    descriptions = models.TextField(default="default_descriptions")
    dimensions_x = models.CharField(max_length=10, default='512')
    dimensions_y = models.CharField(max_length=10, default='512')
    type = models.CharField(max_length=2, default='1')
    style = models.CharField(max_length=50, default='fantasy-art')
    
    def __str__(self):
        return self.asset_name


class Sound_Asset(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='sound_assets')
    soundName = models.CharField(max_length=255, default='default_soundName')
    path = models.CharField(max_length=255, default='default_path')
    descriptions = models.TextField(default='default_descriptions')
    duration = models.CharField(max_length=50, default='10')
    
    def __str__(self):
        return self.soundName


# User Assets Model
class UGAsset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=255, default='New Asset')
    upload_date = models.DateTimeField(default=now)
    file_path = models.CharField(max_length=255, default='path/to/asset')
    status = models.CharField(max_length=100, default='pending review')

# User generated Model
class UGGame(models.Model):
    gameid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    creatorid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_title = models.CharField(max_length=255)
    prompt = models.TextField()
    url = models.URLField(max_length=200)
    default_gameid = models.ForeignKey(Game, on_delete=models.CASCADE)
    asset_list = models.ManyToManyField(UGAsset)
    thumbnail_url = models.URLField(max_length=200)

    def __str__(self):
        return self.game_title
