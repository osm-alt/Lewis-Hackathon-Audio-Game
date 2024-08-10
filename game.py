import pygame
import sys
from audio_to_img import save_sound_wave_image

# Function to display the start screen
def start_screen():
    # Set up font and colors
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    
    # Fill the screen with background color
    screen.fill(bg_color)
    
    # Render the title text
    title_text = font.render("Start Screen", True, text_color)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 100))
    
    # Render the instruction text
    instruction_text = small_font.render("Press SPACE to Start", True, text_color)
    screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + 50))
    
    pygame.display.flip()
    
    # Wait for the user to press the SPACE key to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Main game loop
def main_game():
    # Resize the screen to the dimensions of the background image
    global screen
    screen = pygame.display.set_mode((background.get_width(), background.get_height()))
    
    # Play the audio
    pygame.mixer.music.play()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw the background image
        screen.blit(background, (0, 0))
        
        # Update the display
        pygame.display.flip()
    
    # Quit Pygame
    pygame.quit()
    sys.exit()



# Example usage
audio_file = './output.wav'  # Replace with your audio file path
output_image_file = 'sound_wave.png'  # The image file to save
save_sound_wave_image(audio_file, output_image_file)

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame with Start Screen")

# Load the sound wave image for the background
background = pygame.image.load('sound_wave.png')

# Load the audio file
pygame.mixer.music.load('output.wav')

# Run the start screen
start_screen()

# Run the main game
main_game()