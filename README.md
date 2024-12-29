# Catch the Chaos

## Game Description

"Catch the Chaos" is an interactive hand gesture-based game where players use their hands to catch falling objects within a set time limit. The game features three difficulty levels, allowing players to choose their desired challenge.

## Gameplay

- The game utilizes a camera to detect the player's hand movements.
- Players need to catch falling objects by moving their hand to intercept them before they hit the bottom of the screen.
- Each successful catch earns the player points.
- As the game progresses, the falling objects increase in speed and quantity, increasing the difficulty.

## Gameplay Screenshots
![Screenshot 2024-12-30 025418](https://github.com/user-attachments/assets/d75fbe7b-2e74-4a33-80b9-b6c49a7aa471)
![Screenshot 2024-12-30 025350](https://github.com/user-attachments/assets/dead1064-0de0-4e58-832c-6b05caf99006)
![Screenshot 2024-12-30 025450](https://github.com/user-attachments/assets/f4b73db0-2349-4688-b630-1b6bf888e597)
![Screenshot 2024-12-30 025512](https://github.com/user-attachments/assets/552dfb38-fadf-4f80-938f-afa20df8e1e5)
![Screenshot 2024-12-30 025530](https://github.com/user-attachments/assets/5e4eef0b-44d5-4366-95e1-d341c5f09a1b)
![Screenshot 2024-12-30 025429](https://github.com/user-attachments/assets/769794d4-e320-4d6e-bead-2062782b2bfa)
![Screenshot 2024-12-30 025441](https://github.com/user-attachments/assets/d7a271a9-6828-4a57-9ade-5ebc235051b5)

## Features

- **Hand Gesture Recognition**: The game employs a camera to track the player's hand movements and register catches.
- **Three Difficulty Levels**: Players can choose from Easy, Medium, and Hard difficulties, catering to different skill levels.
- **Leaderboard**: The leaderboard displays the top scores for each difficulty level, fostering competition among players.
- **Achievements**: The game features achievements for specific milestones achieved during gameplay, providing additional goals and rewards.

## Controls

- All types of controls involve keyboard inputs

## Installation

The game is likely written in Python and require libraries like OpenCV for computer vision, pymongo for database management and mediapipe. Follow the steps below to install and set up the game:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/catch-the-chaos.git
   cd catch-the-chaos
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Dependencies

- Python
- OpenCV
- Pygame
- Additional libraries as specified in `requirements.txt`

## Troubleshooting

- **Hand Detection Issues**:
  - Ensure that your camera is properly connected and functioning.
  - Adjust lighting conditions to optimize camera performance.
  - Check the game's configuration settings for any potential issues related to hand detection or calibration.

## Game Developer

- **Name**: Sachin

Enjoy the game!

