
# prompt-to-game

Welcome to `prompt-to-game`, a cutting-edge backend platform designed to transform your textual ideas into interactive, AI-generated games. This project harnesses the power of `Django` and Django REST Framework (DRF), along with advanced AI technologies such as `GPT-4, Stable Diffusion, and ControlNet`, to create a seamless bridge between your imagination and a personalized gaming experience. It uses `firebase` for user-authentication and `Postgres SQL` as the underlying database.

## Overview

`prompt-to-game` leverages textual prompts to dynamically generate unique games, deploying them instantly on Netlify. Our system uses Firebase for robust authentication, PostgreSQL for secure data storage, and a Django-based backend for seamless integration and processing. 

## Features

- **AI-Powered Game Generation**: Utilize advanced AI models like GPT-4, Stable Diffusion, and ControlNet to turn textual prompts into playable games.
- **Secure Authentication**: Implements Firebase for a comprehensive and secure authentication process.
- **Persistent Storage**: Leverages PostgreSQL for reliable storage of user data and generated games.
- **Automatic Deployment**: Automatically deploys generated games to Netlify, providing users with instant access to their creations.
- **User Dashboard**: Offers a comprehensive dashboard for users to manage their prompts, view generated games, and access deployment links.

## Getting Started

### Prerequisites

- Python (version 3.8 or later)
- PostgreSQL
- Firebase account
- Netlify account

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Addy-codes/prompt-to-game.git
cd prompt-to-game
```

2. Set up a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Apply the migrations to your database:

```bash
python manage.py migrate
```

2. Start the Django development server:

```bash
python manage.py runserver
```

The server will start and be available at `http://localhost:8000`.

3. To generate a game, make a POST request to `/prompt` with a JSON body containing your prompt:

```json
{
  "prompt": "A puzzle game set in a post-apocalyptic world"
}
```

## Acknowledgments

- Thanks to OpenAI for GPT-4, and the teams behind Stable Diffusion and ControlNet for their incredible AI models.
- Firebase, PostgreSQL, and Netlify for their robust services that support this project's infrastructure.

Explore `prompt-to-game` and unleash the power of your creativity. We can't wait to see the games you'll create!

