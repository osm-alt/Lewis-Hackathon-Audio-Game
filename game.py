import pygame
import sys
from audio_to_img import save_sound_wave_image

# Define the Sprite class
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Red square
        self.rect = self.image.get_rect()
        self.rect.y = background.get_height() // 2  # Start in the middle of the y-axis
        self.rect.x = 0  # Start on the left side

    def update(self):
        self.rect.x += 1  # Move the sprite to the right
        if self.rect.right > background.get_width():
            self.rect.left = 0  # Reset to the left side when it reaches the end

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
    screen.blit(title_text, (start_screen_width // 2 - title_text.get_width() // 2, start_screen_height // 2 - 100))
    
    # Render the instruction text
    instruction_text = small_font.render("Press SPACE to Start", True, text_color)
    screen.blit(instruction_text, (start_screen_width // 2 - instruction_text.get_width() // 2, start_screen_height // 2 + 50))
    
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

    # Create a sprite group and add the moving sprite
    all_sprites = pygame.sprite.Group()
    sprite = MovingSprite()
    all_sprites.add(sprite)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the sprite's position
        all_sprites.update()
        
        # Draw the background image
        screen.blit(background, (0, 0))
        
        # Draw all the sprites
        all_sprites.draw(screen)
        
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

# Screen dimensions for the start menu
start_screen_width = 800
start_screen_height = 600


# Set up the initial screen for the start menu
screen = pygame.display.set_mode((start_screen_width, start_screen_height))
pygame.display.set_caption("Pygame with Start Screen")

# Load the sound wave image for the background
background = pygame.image.load('sound_wave.png')

# Load the audio file
pygame.mixer.music.load('output.wav')

# Run the start screen
start_screen()

# Run the main game
main_game()