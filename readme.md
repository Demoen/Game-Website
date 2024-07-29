# Olympiad Fighter

This web application is designed for a gaming community, providing an interface to manage and overview video game competitions. It allows users to track who plays against whom, the games they play, and their scores. The website does not play games itself but offers a comprehensive overview and management of the gaming competitions.

![[Pasted image 20240729133019.png]]

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Home Page**: Displays a list of games with details.
- **Game Start Page**: Allows users to start a new game.
- **Join Game Page**: Enables users to join existing games.
- **Static Assets**: Includes images, audio, avatars, and backgrounds to enhance the user experience.
## Screenshots

![[Pasted image 20240729133131.png]]


![[Pasted image 20240729133258.png]]

![[Pasted image 20240729133337.png]]


## Project Structure

```plaintext
Game-Website/
├── game/
│   ├── static/
│   │   ├── audio/           # Audio files for game events
│   │   ├── avatars/         # User avatars
│   │   ├── background/      # Background images
│   │   └── images/          # Game-related images
│   ├── templates/           # HTML templates for the web pages
│   │   ├── game-start.html  # Template for the game start page
│   │   ├── game.html        # Template for the game page
│   │   ├── home-img.html    # Template for home images
│   │   ├── home.html        # Template for the home page
│   │   └── join.html        # Template for the join game page
│   ├── __init__.py          # Initialize the Flask app
│   └── routes.py            # Define routes for the web app
├── requirements.txt         # List of dependencies
└── wsgi.py                  # Entry point for the WSGI server
```

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Game-Website.git
    cd Game-Website
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**
    ```bash
    python wsgi.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to see the home page.

## Screenshots

### Home Page
![Home Page](screenshots/home.png)
*The home page displays a list of available games with images and descriptions.*

### Game Start Page
![Game Start Page](screenshots/game-start.png)
*The game start page allows users to initiate a new game.*

### Join Game Page
![Join Game Page](screenshots/join.png)
*The join game page lets users join an existing game by entering a game code.*

## Contributing

We welcome contributions to improve this project! Here's how you can help:

1. **Fork the repository.**
2. **Create a new branch:**
    ```bash
    git checkout -b feature-branch
    ```
3. **Make your changes and commit them:**
    ```bash
    git commit -m "Description of your changes"
    ```
4. **Push to the branch:**
    ```bash
    git push origin feature-branch
    ```
5. **Submit a pull request.**


