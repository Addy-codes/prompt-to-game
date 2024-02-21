import gradio_client
import shutil
import zipfile
import os
import requests
from chaotix.config import (
    NETLIFY_ACCESS_TOKEN,
    CLIPDROP_API_KEY
)
from firebase_admin import storage
import os
import firebase_admin
from firebase_admin import credentials, storage
import uuid

# Initialize the Gradio client

# client = gradio_client.Client(
#     "https://eccv2022-dis-background-removal.hf.space/--replicas/89iey/")

SITE_ID = None  # Leave as None if creating a new site
# API Endpoints
DEPLOY_URL = f'https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys' if SITE_ID else 'https://api.netlify.com/api/v1/sites'


def remove_background(file_path):
    url = 'https://clipdrop-api.co/remove-background/v1'
    print(CLIPDROP_API_KEY)

    with open(file_path, 'rb') as image_file:
        files = {'image_file': (file_path, image_file, 'image/png')}
        headers = {'x-api-key': CLIPDROP_API_KEY}

        response = requests.post(url, files=files, headers=headers)

        if response.ok:
            # Save the output image back to the original file path
            with open(file_path, 'wb') as out_file:
                out_file.write(response.content)
            print(f"Background removed and image saved back as '{file_path}'")
        else:
            print(f"Error: {response.json()['error']}")

# def remove_background(file_path):
#     # Get the public URL of the image
#     image_url = get_public_url(file_path)

#     # Call the API to remove the background
#     result = client.predict(image_url, api_name="/predict")
#     processed_image_path = result[0]

#     # Replace the original file with the new file
#     shutil.move(processed_image_path, file_path)

#     print(file_path)

#     temp_dir = os.path.dirname(processed_image_path)
#     if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
#         shutil.rmtree(temp_dir)


def get_public_url(file_path):
    """
    Uploads a file to 0x0.st and returns the URL.

    :param file_path: Path to the file to upload
    :return: URL of the uploaded file
    """
    with open(file_path, 'rb') as f:
        response = requests.post('https://0x0.st', files={'file': f})

    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Error uploading file: {response.status_code}")


# Create a ZIP file of the website folder
def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(
                    os.path.join(root, file), os.path.join(folder_path, '..')))

# Deploy the site using the ZIP file


def deploy_site(zip_path):
    headers = {
        'Content-Type': 'application/zip',
        'Authorization': f'Bearer {NETLIFY_ACCESS_TOKEN}'
    }
    with open(zip_path, 'rb') as zipf:
        response = requests.post(DEPLOY_URL, headers=headers, data=zipf)
    return response.json()


def upload_to_firebase(user_id, game_name, local_path, firebase_directory):
    """
    Uploads a file or all files in a folder to Firebase Storage under a specific user's directory and returns their public URLs.

    :param user_id: Unique identifier for the user, used to create a user-specific folder in Firebase.
    :param local_path: The local path of the file or folder to upload.
    :param firebase_directory: The base directory in Firebase where the files will be uploaded.
    :return: Public URL of the uploaded file for single file uploads, None for folder uploads.
    """
    bucket = storage.bucket("chaotix-c07af.appspot.com")

    def upload_file(file_path, firebase_path):
        blob = bucket.blob(firebase_path.replace("\\", "/")
                           )  # Ensure using forward slashes
        blob = bucket.blob(firebase_path)
        blob.upload_from_filename(file_path)
        blob.make_public()
        return blob.public_url

    if os.path.isdir(local_path):
        for root, dirs, files in os.walk(local_path):
            for filename in files:
                # Construct the file path within Firebase, preserving the local folder structure
                file_path = os.path.join(root, filename)
                firebase_path = os.path.join(
                    firebase_directory, user_id, os.path.relpath(root, local_path), filename)
                upload_file(file_path, firebase_path)
        # No URL is returned for folder uploads
        return None
    elif os.path.isfile(local_path):
        # Single file upload
        unique_id = str(uuid.uuid4())
        firebase_path = f"{firebase_directory}/{user_id}/{game_name}/{unique_id}.png"
        url = upload_file(local_path, firebase_path)
        return url
    else:
        raise ValueError('Invalid path provided')
