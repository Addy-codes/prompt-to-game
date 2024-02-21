
from django.core.management.base import BaseCommand, CommandError
from game.models import Game, Image_Assets,Sound_Asset
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Fills the database with game, image, and sound data from game_data.json.'

    def add_arguments(self, parser):
        # Optional: Add an argument to specify a different file path
        parser.add_argument('--file', type=str, help='Path to the JSON file with game data', default='game_data.json')

    def handle(self, *args, **options):
        file_path = options['file']

        # Ensure the file exists
        if not Path(file_path).exists():
            raise CommandError(f'The file {file_path} does not exist.')

        # Load the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Assuming data is a list of game data dictionaries
        for game_data in data:
            game = Game.objects.create(
                game_name=game_data['game_name'],
                descriptions=game_data['descriptions'],
                search_descriptions=game_data['search_descriptions']
            )

            for image_asset in game_data.get('image_asset', []):
                Image_Assets.objects.create(
                    game=game,
                    asset_name=image_asset['asset_name'],
                    path=image_asset['path'],
                    descriptions=image_asset['descriptions'],
                    dimensions_x=image_asset['dimensions_x'],
                    dimensions_y=image_asset['dimensions_y'],
                    type=image_asset['type'],
                    style=image_asset['style']
                )

            for sound_asset in game_data.get('sound_assets', []):
                Sound_Asset .objects.create(
                    game=game,
                    soundName=sound_asset['soundName'],
                    path=sound_asset['path'],
                    descriptions=sound_asset['descriptions'],
                    duration=sound_asset['duration']
                )

        self.stdout.write(self.style.SUCCESS('Successfully inserted game data from JSON file'))

