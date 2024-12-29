import pygame
import cv2
import mediapipe as mp
import pymongo
import random 

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HandGestureGame"]
users_collection = db["Users"]  
achievements_collection = db["Achievements"]  
leaderboard_collection = db["Leaderboard"]

pygame.init()
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h  
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN) 
pygame.display.set_caption("Catch the Falling Objects")
clock = pygame.time.Clock()


background_image = pygame.image.load("image.png")  
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  

gray = (200, 200, 200)  
yellow = (255, 255, 0) 
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREEN = (144, 238, 144)
LIGHTBLUE = (173, 216, 230)
LIGHTRED = (255, 182, 193)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 74)

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

# User Profiles
user_profiles = {}

# Define achievements
achievements = {
    "First Catch": {"description": "Catch your first falling object.", "completed": False},
    "Score 10": {"description": "Reach a score of 10.", "completed": False},
    "Score 50": {"description": "Reach a score of 50.", "completed": False},
    "Score 100": {"description": "Reach a score of 100.", "completed": False},
}

# Particle class to handle individual particles
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)  # Random size for particles
        self.color = (255, 255, 0)  # Yellow color
        self.lifetime = random.randint(20, 50)  # Lifetime in frames
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random direction

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime -= 1  # Decrease lifetime

    def is_alive(self):
        return self.lifetime > 0

# Function to create particles
def create_particles(x, y, num_particles=10):
    return [Particle(x, y) for _ in range(num_particles)]

# Function to load user profiles from MongoDB
def load_user_profiles():
    global user_profiles
    user_profiles = {}
    for user in users_collection.find():
        user_profiles[user['username']] = {
            "score": user.get("score", 0),
            "achievements": user.get("achievements", [])
        }

# Function to save user profiles to MongoDB
def save_user_profiles():
    for username, profile in user_profiles.items():
        users_collection.update_one(
            {"username": username},
            {"$set": {"score": profile["score"], "achievements": profile["achievements"]}},
            upsert=True
        )

# Function: Display Text (Updated for Centering)
def display_text(text, x, y, color, size="medium"):
    text_surface = font.render(text, True, color) if size == "medium" else large_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))  # Center the text
    screen.blit(text_surface, text_rect)


# Function: Display Leaderboard (Updated to Show All Difficulties)
def display_leaderboard():
    background_image = pygame.image.load("leader.png")  # Ensure this file exists in the working directory
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to fit the screen
    screen.blit(background_image, (0, 0))  # Draw background image
    #display_text("Leaderboard", screen_width // 2, 50, yellow, size="large")

    difficulties = ["Easy", "Medium", "Hard"]
    y_offset = 100  # Starting position for displaying scores

    for difficulty in difficulties:
        display_text(f"{difficulty} Difficulty", screen_width // 2, y_offset, yellow, size="medium")
        y_offset += 30  # Space between difficulty titles

        # Fetch top scores based on difficulty
        top_scores = leaderboard_collection.find({"difficulty": difficulty}).sort("score", -1).limit(5)
        for idx, entry in enumerate(top_scores):
            display_text(f"{entry['username']} - {entry['score']}", screen_width // 2, y_offset, gray)
            y_offset += 30  # Space between scores

        y_offset += 20   # Extra space between different difficulty sections

    #display_text("Press ENTER to return to the main menu", screen_width // 2, y_offset, WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# Function: Display Home Screen
def display_home_screen():
    # Load background image
    bg = pygame.image.load("homescreen.png")  # Replace with your image path
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter key
                    return "start_game"
                if event.key == pygame.K_l:  # View leaderboard on 'L' key
                    return "view_leaderboard"
                if event.key == pygame.K_a:  # View achievements on 'A' key
                    return "view_achievements"
                if event.key == pygame.K_ESCAPE:  # Exit on Escape key
                    pygame.quit()
                    exit()

        # Draw the background image
        screen.blit(bg, (0, 0))

        # Draw title
        #title_font = pygame.font.Font(None, 74)
        #title_text = title_font.render("CATCH THE CHAOS", True, yellow)  # Light gray
        #title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        #screen.blit(title_text, title_rect)

        # Draw buttons with the specified colors
        #button_font = pygame.font.Font(None, 48)

        # Define colors
        #gray = (200, 200, 200)  # Light gray
        #yellow = (255, 255, 0)  # Yellow color

        # Draw buttons using the specified colors
        #screen.blit(button_font.render("Press ENTER to Start", True, gray_color), (screen_width // 2, screen_height // 2))
        #screen.blit(button_font.render("Press L for Leaderboard", True, yellow_color), (screen_width // 2, screen_height // 2 + 50))
        #screen.blit(button_font.render("Press A for Achievements", True, gray_color), (screen_width // 2, screen_height // 2 + 100))
        #screen.blit(button_font.render("Press ESC to Exit", True, yellow_color), (screen_width // 2, screen_height // 2 + 150))
        #button_font = pygame.font.Font(None, 48)
        #start_text = button_font.render("Press ENTER to Start", True, WHITE)
        #leaderboard_text = button_font.render("Press L for Leaderboard", True, WHITE)
        #achievements_text = button_font.render("Press A for Achievements", True, WHITE)
        #exit_text = button_font.render("Press ESC to Exit", True, WHITE)

        # Position buttons
        #start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        #leaderboard_rect = leaderboard_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        #achievements_rect = achievements_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        #exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))

        # Draw buttons
        #screen.blit(start_text, start_rect)
        #screen.blit(leaderboard_text, leaderboard_rect)
        #screen.blit(achievements_text, achievements_rect)
        #screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        clock.tick(60)  # Maintain frame rate

# Function: Register or Log In with Profile Management
def register_or_login_user():
    bg = pygame.image.load("name.png")  # Replace with your image path
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    screen.fill(BLACK)
    screen.blit(bg, (0, 0))
    #display_text("Enter Username: ", screen_width // 2 - 150, screen_height // 2 - 50, yellow)
    pygame.display.flip()

    username = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]  # Remove last character
                else:
                    username += event.unicode  # Add new character

        # Clear the screen and redraw the prompt and username
        screen.fill(BLACK)
        screen.blit(bg, (0, 0)) 
        #display_text("Enter Username: ", screen_width // 2 - 150, screen_height // 2 - 50, yellow)
        
        # Display the current username
        display_text(username, screen_width // 2 - 150, screen_height // 2, gray)  # Display username in green

        pygame.display.flip()  # Update the display

    # Load user profile from MongoDB
    user_profile = users_collection.find_one({"username": username})
    if user_profile:
        print(f"Welcome back, {username}!")
    else:
        print("User registered successfully!")
        user_profile = {"username": username, "score": 0, "achievements": []}
        users_collection.insert_one(user_profile)

    # Load achievements into user_profiles
    user_profiles[username] = {
        "score": user_profile.get("score", 0),
        "achievements": user_profile.get("achievements", [])
    }

    return username


# Function: Game Over Screen (Updated for Alignment)
def game_over_screen(score, username, difficulty):
    background_image = pygame.image.load("over.png")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(background_image, (0, 0))
    #display_text("Game Over!", screen_width // 2, screen_height // 4, yellow, size="large")  # Red color for Game Over
    display_text(f"Your Score: {score}", screen_width // 2, screen_height // 2 - 30, gray)  # Green color for score

    # Retrieve existing record or initialize new entry
    user_record = leaderboard_collection.find_one({"username": username, "difficulty": difficulty})
    if not user_record:
        leaderboard_collection.insert_one({"username": username, "score": score, "difficulty": difficulty})
        current_high_score = score
    else:
        current_high_score = user_record['score']
        if score > current_high_score:
            leaderboard_collection.update_one(
                {"username": username, "difficulty": difficulty},
                {"$set": {"score": score}}
            )
            current_high_score = score

    # Fetch overall highest score for the difficulty
    overall_high_score_entry = leaderboard_collection.find({"difficulty": difficulty}).sort("score", -1).limit(1)
    overall_high_score = 0
    overall_high_username = ""
    for entry in overall_high_score_entry:
        overall_high_score = entry['score']
        overall_high_username = entry['username']

    display_text(f"Your High Score: {current_high_score}", screen_width // 2, screen_height // 2 + 30, gray)  # White color
    display_text(f"Overall High Score: {overall_high_score} by {overall_high_username}", screen_width // 2, screen_height // 2 + 70, gray)  # White color
    #display_text("Press R to Restart or M for Main Menu", screen_width // 2, screen_height // 2 + 110, gray)  # White color
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return "restart"
                if event.key == pygame.K_m:  # Return to main menu
                    return "menu"


def display_webcam_frame(frame):
    frame = cv2.flip(frame, 0)  # Flip vertically (0 for x-axis flip)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    #frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (150, 200))  # Resize webcam feed
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    frame_surface = pygame.surfarray.make_surface(frame)  # Convert frame to Pygame surface
    screen.blit(frame_surface, (24, 20))  # Draw it in the top-left corner


# Global variable to hold the current message and its display time
current_message = ""
message_display_time = 0  # Time in milliseconds to display the message

# Function: Display Motivational or Sarcastic Message
def display_milestone_message(score):
    global current_message, message_display_time
    messages = [
        "You're on fire! Keep it up!",
        "Is that a score or a phone number?",
        "Wow, look at you go! Are you a pro?",
        "Don't get too cocky, it's just a game!",
        "You're catching those like a pro!",
        "Is this your first time playing? Just kidding!",
        "Keep it up! You're almost a legend!",
        "Did you just hack the game? Nice score!"
    ]
    current_message = random.choice(messages)
    message_display_time = pygame.time.get_ticks() + 2000  # Show for 2 seconds

# Function to shake the screen
def shake_screen(shake_duration=10, shake_intensity=5):
    global shake_offset
    shake_offset = [random.randint(-shake_intensity, shake_intensity), random.randint(-shake_intensity, shake_intensity)]
    for _ in range(shake_duration):
        yield  # Wait for the next frame
    shake_offset = [0, 0]  # Reset offset after shaking

# Function: Main Game Loop (Updated to Check Achievements)
def main_game(username, difficulty):
    bg = pygame.image.load("image.jpg")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    global current_message, message_display_time
    paddle_width = 100
    paddle_height = 20
    paddle_x = screen_width // 2 - paddle_width // 2
    paddle_y = screen_height - 50
    object_width = 30
    object_height = 30
    score = 0
    misses = 0
    max_misses = 3  # Set maximum misses to 3
    falling_objects = []  # List to hold falling objects
    object_timer = 0  # Timer to control object generation
    object_interval = random.uniform(1.0, 3.0)  # Random interval between 1 and 3 seconds
    object_speed = 5  # Set a uniform speed for all falling objects

    # Initialize caught_particles list
    caught_particles = []  # List to hold active particles

    # Set the maximum number of falling objects based on difficulty
    if difficulty == "Easy":
        max_falling_objects = 1
    elif difficulty == "Medium":
        max_falling_objects = random.randint(2, 3)
    else:  # Hard
        max_falling_objects = 3  # You can adjust this to allow more if needed

    running = True
    paused = False  # Variable to track if the game is paused
    shake_offset = [0, 0]  # Initialize shake offset
    shake_active = False  # Flag to check if shaking is active
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for Escape key
                    paused = not paused  # Toggle pause state

        if not paused:  # Only update game state if not paused
            ret, frame = cap.read()
            if not ret:
                print("Webcam feed unavailable!")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            #hand_detected = False
            if results.multi_hand_landmarks:
                #hand_detected = True
                for hand_landmarks in results.multi_hand_landmarks:
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x = index_tip.x  # Normalized (0 to 1)
                    target_x = max(0, min(screen_width - paddle_width, int(x * screen_width - paddle_width / 2)))

                    # Smooth paddle movement
                    paddle_x += (target_x - paddle_x) * 0.1  # Adjust the smoothing factor as needed
                    paddle_x = max(0, min(screen_width - paddle_width, paddle_x))  # Keep paddle within bounds
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Update the timer
            object_timer += clock.get_time() / 1000.0  # Convert milliseconds to seconds

            # Generate new falling objects if the timer exceeds the interval
            if object_timer >= object_interval:
                if len(falling_objects) < max_falling_objects:  # Check if we can add more objects
                    object_x = random.randint(0, screen_width - object_width)
                    falling_objects.append([object_x, -object_height])  # Add new object with uniform speed
                object_timer = 0  # Reset the timer
                object_interval = random.uniform(1.0, 3.0)  # Set a new random interval

            # Update positions of falling objects
            for obj in falling_objects:
                obj[1] += object_speed  # Move object down by uniform speed

                # Check if the object has fallen off the screen
                if obj[1] > screen_height:
                    misses += 1  # Increment misses if the object reaches the bottom
                    falling_objects.remove(obj)  # Remove the object from the list

                    if misses >= max_misses:
                        print("Out of chances!")
                        return game_over_screen(score, username, difficulty)

            # Detect collisions with paddle
            for obj in falling_objects:
                if paddle_x <= obj[0] <= paddle_x + paddle_width and \
                   paddle_y <= obj[1] + object_height <= paddle_y + paddle_height:
                    score += 1
                    caught_particles.extend(create_particles(obj[0] + object_width // 2, obj[1] + object_height // 2))  # Create particles
                    falling_objects.remove(obj)  # Remove the caught object
                    shake_active = True  # Start shaking

                    # Check for milestone scores
                    if score % 10 == 0:  # Example milestone at every 10 points
                        display_milestone_message(score)

            # Draw the background image
            if shake_active:
                for _ in shake_screen():
                    # Draw game elements with shake offset
                    screen.blit(bg, (shake_offset[0], shake_offset[1]))  # Draw background with shake
                    # Draw other game elements here, applying shake_offset to their positions
                    # Example: pygame.draw.rect(screen, GREEN, (paddle_x + shake_offset[0], paddle_y + shake_offset[1], paddle_width, paddle_height))
            else:
                # Draw normally
                screen.blit(bg, (0, 0))  # Draw background normally
                # Draw other game elements here without offset

            # Draw elements
            pygame.draw.rect(screen, yellow, (paddle_x, paddle_y, paddle_width, paddle_height))  # Paddle
            for obj in falling_objects:
                pygame.draw.rect(screen, gray, (obj[0], obj[1], object_width, object_height))  # Falling objects
            score_text = font.render(f"Score: {score}", True, WHITE)
            rect = score_text.get_rect()
            rect.topright = (screen_width - 20, 10)
            screen.blit(score_text, rect)
            display_webcam_frame(frame)  # Display the webcam feed

            # Display the current message if it's time to show it
            if current_message and pygame.time.get_ticks() < message_display_time:
                display_text(current_message, screen_width - 150, 10, WHITE, size="medium")  # Display in top-right corner

        else:
            # Display pause message
            pause_text = font.render("Game Paused. Press ESC to Resume or M for Main Menu.", True, WHITE)
            screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))

            # Check for menu option
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # Check for M key to go to main menu
                        return "menu"  # Return to main menu

        pygame.display.flip()
        clock.tick(60)  # Set to 60 FPS for smoother performance

        # Check for achievements after scoring
        check_achievements(score, username)

    # At the end of the game, display achievements
    display_achievements(username)

    return game_over_screen(score, username, difficulty)


# Function: Display Difficulty Selection Screen
def display_difficulty_selection():
    # Load background image
    background_image = pygame.image.load("diff.png")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Main loop for the difficulty selection screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Select Easy
                    return "Easy"
                if event.key == pygame.K_2:  # Select Medium
                    return "Medium"
                if event.key == pygame.K_3:  # Select Hard
                    return "Hard"
                if event.key == pygame.K_ESCAPE:  # Return to main menu
                    return "menu"

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw title
        '''title_font = pygame.font.Font(None, 74)  # Use a larger font for the title
        title_text = title_font.render("Select Difficulty", True, yellow)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        # Draw difficulty options
        button_font = pygame.font.Font(None, 48)  # Use a smaller font for buttons
        easy_text = button_font.render("1. Easy", True, WHITE)
        medium_text = button_font.render("2. Medium", True, WHITE)
        hard_text = button_font.render("3. Hard", True, WHITE)
        return_text = button_font.render("Press ESC to Return", True, WHITE)

        # Position buttons
        easy_rect = easy_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        medium_rect = medium_text.get_rect(center=(screen_width // 2, screen_height // 2))
        hard_rect = hard_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        return_rect = return_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))

        # Draw buttons
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        screen.blit(return_text, return_rect)

        # Highlight selected option (optional)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if easy_rect.collidepoint((mouse_x, mouse_y)):
            easy_text = button_font.render("1. Easy", True, yellow)  # Change color on hover
        if medium_rect.collidepoint((mouse_x, mouse_y)):
            medium_text = button_font.render("2. Medium", True, yellow)  # Change color on hover
        if hard_rect.collidepoint((mouse_x, mouse_y)):
            hard_text = button_font.render("3. Hard", True, yellow)  # Change color on hover

        # Draw the updated buttons
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)'''

        pygame.display.flip()
        clock.tick(60)  # Maintain frame rate

# Function to check and update achievements
def check_achievements(score, username):
    if username not in user_profiles:
        user_profiles[username] = {"score": 0, "achievements": []}

    # Check for achievements
    if "First Catch" not in user_profiles[username]["achievements"] and score >= 1:
        user_profiles[username]["achievements"].append("First Catch")
        print("Achievement unlocked: First Catch!")

    if "Score 10" not in user_profiles[username]["achievements"] and score >= 10:
        user_profiles[username]["achievements"].append("Score 10")
        print("Achievement unlocked: Score 10!")

    if "Score 50" not in user_profiles[username]["achievements"] and score >= 50:
        user_profiles[username]["achievements"].append("Score 50")
        print("Achievement unlocked: Score 50!")

    if "Score 100" not in user_profiles[username]["achievements"] and score >= 100:
        user_profiles[username]["achievements"].append("Score 100")
        print("Achievement unlocked: Score 100!")

    save_user_profiles()  # Save profiles after checking achievements

# Function to display achievements
def display_achievements(username):
    if username in user_profiles:
        print(f"Achievements for {username}:")
        for achievement in user_profiles[username]["achievements"]:
            print(f"- {achievement}: {achievements[achievement]['description']}")
    else:
        print("No achievements found.")

# Function to Display Achievements and Profile
def display_achievements_screen(username):
    background_image = pygame.image.load("ach.png")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to main menu on ESC
                    running = False

        # Clear the screen
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Draw title
        #title_font = pygame.font.Font(None, 74)
        #title_text = title_font.render("Achievements", True, yellow)
        #title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        #screen.blit(title_text, title_rect)

        # Display achievements
        if username in user_profiles:
            achievements_list = user_profiles[username]["achievements"]
            if achievements_list:
                y_offset = screen_height // 4 + 50  # Start below the title
                for achievement in achievements_list:
                    achievement_text = f"- {achievement}: {achievements[achievement]['description']}"
                    achievement_surface = font.render(achievement_text, True, WHITE)
                    screen.blit(achievement_surface, (screen_width // 2 - achievement_surface.get_width() // 2, y_offset))
                    y_offset += 30  # Space between achievements
            else:
                no_achievements_text = "No achievements found."
                no_achievements_surface = font.render(no_achievements_text, True, WHITE)
                screen.blit(no_achievements_surface, (screen_width // 2 - no_achievements_surface.get_width() // 2, screen_height // 2))
        else:
            no_profile_text = "User profile not found."
            no_profile_surface = font.render(no_profile_text, True, WHITE)
            screen.blit(no_profile_surface, (screen_width // 2 - no_profile_surface.get_width() // 2, screen_height // 2))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Maintain frame rate

# Function to draw a button with hover effect
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))  # Draw hover color
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))  # Draw normal color

    # Render text
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Main Program
username = register_or_login_user()  # Prompt for username first

while True:
    outcome = display_home_screen()

    if outcome == "start_game":
        difficulty = display_difficulty_selection()
        if difficulty in ["Easy", "Medium", "Hard"]:
            main_game(username, difficulty)
        elif difficulty == "menu":
            continue  # Return to the home screen

    elif outcome == "view_leaderboard":
        display_leaderboard()
    
    elif outcome == "view_achievements":
        display_achievements_screen(username)  # Show achievements screen


