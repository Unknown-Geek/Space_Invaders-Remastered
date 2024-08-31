# Space Invaders Remastered

Welcome to Space Invaders Remastered! This is a modern take on the classic arcade game, featuring AI hand tracking for controls and a high score system using SQLite.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## Features
- Classic Space Invaders gameplay
- AI hand tracking for player controls
- High score system with SQLite database
- Scrolling background and sound effects
- Leaderboard and latest scores display
- Instructions page

## Installation

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Clone the Repository
```bash
git clone https://github.com/yourusername/space_invaders_remastered.git
cd space_invaders_remastered
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Additional Setup
Ensure you have a webcam connected for AI hand tracking. Place the required images and sound files in the project directory:
- `background.jpg`
- `ufo.png`
- `arcade-game.png`
- `bullet (1).png`
- `icons8-spaceship-64.png`
- `background.wav`
- `game_over.mp3`
- `explosion.wav`
- `laser.wav`

## Usage
Run the game using the following command:
```bash
python main.py
```

## Controls
- **Right Hand**: Tilt left or right to move the player.
- **Left Hand**: Show all fingers to shoot bullets.
- **Keyboard**: Press ESC to return to the main menu or quit the game.

## Screenshots
- Main Menu
  ![{F9E4D76D-E433-4E08-A5BC-C5BDE056AA91}](https://github.com/user-attachments/assets/34936cec-9e6e-4815-8f62-4a67ab318c10)

- Gameplay
  ![{12F32035-5859-43FB-AC20-35E09647422C}](https://github.com/user-attachments/assets/f4a764d8-addc-4cea-8c0e-b8fdeb91dfd1)

- Scores
  ![{073797AC-5F0A-4521-9D84-3275C80CE1E3}](https://github.com/user-attachments/assets/13c2a50b-5dad-49ad-a8f0-94b95c7976c9)

- Instructions
  ![{7CC1AE74-191A-4F62-B776-F44CC516871E}](https://github.com/user-attachments/assets/93548054-6814-42bf-8892-3b1903ed7172)

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.
