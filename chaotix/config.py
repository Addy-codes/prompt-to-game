import json

with open(f'./keys/config.json') as f:
    config = json.load(f)

POSTGRES_PASS = config['postgres_pass']
STABILITY_API_KEY = config['stability_api_key']
CLIPDROP_API_KEY = config['clipdrop_api_key']
OPENAI_API_KEY = config['openai_api_key']
NETLIFY_ACCESS_TOKEN = config['netlify_access_token']