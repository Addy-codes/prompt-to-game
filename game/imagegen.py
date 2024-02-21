import base64, requests
from PIL import Image
from game.helper import *
from chaotix.config import(
    STABILITY_API_KEY
)

def generate_spritesheet(prompt, style, sprite_dir, output_dir, x, y):
    tempx, tempy = get_payload_dimensions(x, y)
    
    resized_image = resize_image(sprite_dir, (tempx, tempy))
    save_image(resized_image, sprite_dir)

    data = {
        "init_image_mode": "IMAGE_STRENGTH",
        "image_strength": 0.05,
        "steps": 40,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "style_preset": style,
        "text_prompts[0][text]": prompt,
        "text_prompts[0][weight]": 1,
        "text_prompts[1][text]": 'blurry, bad',
        "text_prompts[1][weight]": -1,
    }

    mtmgenerate(data, sprite_dir, output_dir, prompt, 0.05)
    remove_background(output_dir)
    resized_img = resize_image(output_dir, (x , y))
    save_image(resized_img, output_dir)
    crop_blank_spaces(output_dir)

def generate_image(prompt, style, img_path, x, y):
    tempx, tempy = get_payload_dimensions(x, y)
    image_generation_body = {
        "steps": 40,
        "width": tempx,
        "height": tempy,
        "seed": 0,
        "cfg_scale": 7,
        "samples": 1,
        "style_preset": style,
        "text_prompts": [
            {
            "text": f"{prompt}",
            "weight": 1
            },
            {
            "text": "blurry, bad",
            "weight": -1
            }
        ],
    }
    # Generate image
    generated_data = ttmgenerate_image(image_generation_body)
    for i, image in enumerate(generated_data["artifacts"]):

        # Decode the base64 image
        decoded_image = base64.b64decode(image["base64"])

        # Write to the original path
        with open(img_path, "wb") as f:
            f.write(decoded_image)


def ttmgenerate_image(body):
    url="https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    return response.json()

def mtmgenerate(data, image_path, output_dir, prompt, image_strength):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {STABILITY_API_KEY}"}
    files = {"init_image": open(image_path, "rb")}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for image in data["artifacts"]:
        with open(output_dir, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

def get_payload_dimensions(x, y):
    tempx = 1024
    tempy = 1024

    if x // y >= 2:
        tempx = 1536
        tempy = 640
    elif y // x >= 2:
        tempx = 640
        tempy = 1536
    
    return tempx, tempy

def resize_image(file_path, new_size):
    with Image.open(file_path) as img:
        resized_image = img.resize(new_size)
        return resized_image

def crop_blank_spaces(file_path):
    # Open the image
    img = Image.open(file_path)
    
    # Get the bounding box and crop the image
    bbox = img.getbbox()

    if bbox:  # Check if there is a non-zero bounding box
        cropped_img = img.crop(bbox)
        
        # Save the cropped image
        cropped_img.save(file_path)
        print(f"Cropped and saved: {file_path}")

def save_image(image, file_path):
    image.save(file_path)