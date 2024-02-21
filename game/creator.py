import json
from openai import OpenAI
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from game.helper import *
from game.imagegen import *
from .models import *
from chaotix.config import (
    OPENAI_API_KEY
)

# # AWS SES configuration
# AWS_REGION = "eu-north-1"  # e.g., 'us-west-2'
# SENDER_EMAIL = "ankurg@gmail.com"  # This should be a verified email in AWS SES


def createGame(theme, user_id):
    print("Finding choice")
    most_similar_game_id, most_similar_game = find_most_similar_game(theme)
    # most_similar_game_id, most_similar_game = 13,"Jumpyball"
    prompt, image_assets = format_prompt(most_similar_game_id, theme)
    print(f"Prompt: {prompt}")
    game_directory = f"./games/Custom{most_similar_game}/"
    processed_theme = process_theme(prompt)
    # print("processed_theme: ", processed_theme)
    parsed_theme = parse_processed_theme(processed_theme)
    # print("parsed_theme: ",parsed_theme)

    # image_assets = get_image_assets(most_similar_game)
    print("\n------------------image_assets------------------")
    thumbnail_url = generate_thumbnail(user_id, most_similar_game, parsed_theme['thumbnail'], game_directory)
    generate_assets(image_assets, parsed_theme)
    folder_path = f'./games/Custom{most_similar_game}'
    zip_path = f'./games/_game_zips_/{most_similar_game}_website.zip'
    url = deploy(folder_path, zip_path)

    # Saving to Postgres
    creator_user_instance = CustomUser.objects.get(firebase_uid=user_id)
    game_instance = Game.objects.get(id=most_similar_game_id)
    UGGame.objects.create(
        creatorid_id=creator_user_instance.firebase_uid,
        game_title=parsed_theme['title'],
        prompt=theme,
        url=url,
        thumbnail_url=thumbnail_url,
        default_gameid_id=game_instance.id 
    )

    return parsed_theme['title'], parsed_theme['description'], thumbnail_url, url


def find_most_similar_game(user_description):
    games = Game.objects.all()
    prompt = {}
    game_id_map = {}  # Dictionary to map game names to their IDs

    # Iterate over each Game object to construct the prompt dictionary and map game names to IDs
    for game in games:
        # Use game_name as the key for the prompt dictionary
        prompt[game.game_name] = game.search_descriptions
        # Map game_name to game.id
        game_id_map[game.game_name] = game.id

    # Preprocess and vectorize the game descriptions
    vectorizer = TfidfVectorizer()  # Add your preprocess_description function as the preprocessor if needed
    game_vectors = vectorizer.fit_transform(prompt.values())

    # Preprocess and vectorize user description
    user_vector = vectorizer.transform([user_description])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_vector, game_vectors)
    
    # Find the index of the game with the highest similarity score
    most_similar_game_index = np.argmax(similarity_scores)

    # Use the index to find the corresponding game name from the keys of the prompt dictionary
    most_similar_game_name = list(prompt.keys())[most_similar_game_index]

    # Retrieve the ID of the most similar game using the game_id_map
    most_similar_game_id = game_id_map[most_similar_game_name]

    print(f"The most similar game in our collection is: {most_similar_game_name} with ID: {most_similar_game_id}")

    return most_similar_game_id, most_similar_game_name


def preprocess_description(description):
    # Add your preprocessing steps here (like tokenization, removing stopwords)
    return description


def format_prompt(most_similar_game_id, theme):
    game = Game.objects.get(id=most_similar_game_id)
    game_name = game.game_name

    # This should be dynamic and removed from here
    prompt = f"Given the theme '{theme}' for a {game_name}, make sure the elements follow the theme, keep the description short and precise. Return response in \"key:value\" pair."
    prompt += f"\n1. title: Generate a short title for this game."
    prompt += f"\n2. description: Generate a short description/plot for the game considering the theme as {theme} for the {game_name} game."
    prompt += f"\n3. thumbnail: Generate a description of the thumbnail considering the theme as {theme} for the {game_name} game."

    image_assets = Image_Assets.objects.filter(game_id=most_similar_game_id)
    counter = 3
    for asset in image_assets:
        counter += 1
        asset_name = asset.asset_name 
        asset_description = asset.descriptions  
        prompt += f"\n{counter}. {asset_name}: {asset_description}."

    prompt += f"\nGenerate above {counter} assets."
    # Remove the last comma and space
    prompt = prompt.rstrip(', ')

    return prompt, image_assets


def process_theme(prompt):
    # openai.api_key = OPENAI_API_KEY
    openaiClient = OpenAI(
        # This is the default and can be omitted
        api_key=OPENAI_API_KEY,
    )
    response = openaiClient.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )
    print("\n--------------processed_response------------------")
    processed_response = response.choices[0].message.content
    print(processed_response)
    return processed_response


def parse_processed_theme(processed_theme_str):
    theme_dict = {}
    lines = processed_theme_str.split('\n')

    for line in lines:
        if not line.strip():  # Skip empty lines
            continue
        # Splitting the line at the first ':' to separate key and value
        split_line = line.split(':', 1)
        if len(split_line) != 2:  # Skip any lines that don't match the expected format
            continue
        key, value = split_line
        # Removing serial number and period from the key, and trimming whitespace
        key = key.split('. ', 1)[-1].strip()
        # Trim leading and trailing whitespace and quotes from the value
        value = value.strip().strip('"')
        theme_dict[key] = value

    print("\n--------------parsed_processed_theme------------------")
    print(theme_dict)
    return theme_dict


def get_image_assets(game_name):
    # Read the JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Check if the game name exists in the data
    if game_name in data:
        game_data = data[game_name]

        # Extract image assets from the game data
        image_assets = game_data.get('data', [])

        return image_assets
    else:
        return "Game not found."


def generate_thumbnail(user_id, game_name, prompt, game_directory):
    print("Generating Thumbnail")
    generate_image(prompt, "fantasy-art",
                   f"{game_directory}Customthumbnail.png", 1024, 1024)
    # thumbnail_url = get_public_url(f"{game_directory}Customthumbnail.png")
    thumbnail_url = upload_to_firebase(user_id=user_id, game_name=game_name, local_path=f"{game_directory}Customthumbnail.png", firebase_directory="thumbnails")
    return thumbnail_url


def generate_assets(image_assets, parsed_theme):
    for asset in image_assets:
        asset_name = asset.asset_name
        path = asset.path
        x = int(asset.dimensions_x)
        y = int(asset.dimensions_y)
        asset_type = asset.type
        style = asset.style
        print("Generating : ", asset_name)
        # Depending on the type of asset, call the appropriate function
        if asset_type == "1":
            # Generate the image and then remove the background
            generate_image(parsed_theme[asset_name], style, path, x, y)
            remove_background(path)

            resized_img = resize_image(path, (x, y))
            save_image(resized_img, path)

            # Implement Cropping
            crop_blank_spaces(path)

        elif asset_type == "2":
            # Generate the image without removing the background
            generate_image(parsed_theme[asset_name], style, path, x, y)
            resized_img = resize_image(path, (x, y))
            save_image(resized_img, path)
        elif asset_type == "3":
            # Generate a spritesheet
            sprite_path = path.rsplit(
                '/', 1)[0] + '/sprite_template/' + path.rsplit('/', 1)[1]
            generate_spritesheet(
                parsed_theme[asset_name], style, sprite_path, path, x, y)
        else:
            print(f"Unknown type for asset {asset_name}")


def deploy(folder_path, zip_path):
    # Zip the website folder
    zip_folder(folder_path, zip_path)

    # Deploy the site
    deploy_response = deploy_site(zip_path)
    if 'url' in deploy_response:
        url = deploy_response['url']
        print(f"Deployment Completed. Deploy URL: {url}")

    else:
        print("Error in deployment:", deploy_response)
        return "Error in deployment"
    return url
