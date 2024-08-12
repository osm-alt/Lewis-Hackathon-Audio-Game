import pygame
import sys
from audio_to_img import save_sound_wave_image

# Define the Sprite class with jumping capability
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Red square
        self.rect = self.image.get_rect()
        self.rect.y = background.get_height() // 2  # Start in the middle of the y-axis
        self.rect.x = 0  # Start on the left side

        # Initialize physics variables
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -5
        self.is_jumping = False
        self.on_ground = True
        self.is_moving = True
        self.speed = speed  # Movement speed of the sprite
        self.has_jumped = False  # Track if the sprite has jumped

    def update(self, delta_time):
        if self.is_moving:
            # Move the sprite to the right based on the speed and delta_time
            self.rect.x += self.speed * delta_time
            
            # Stop the sprite if it reaches the right edge of the screen
            if self.rect.right >= background.get_width():
                self.rect.right = background.get_width()
                self.is_moving = False

        # Apply gravity if the sprite has jumped at least once and is not on the ground
        if self.has_jumped and not self.is_jumping:
            self.y_velocity += self.gravity

        # Update the vertical position
        self.rect.y += self.y_velocity

        # Prevent the sprite from going above the top of the screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y_velocity = 0

        # Check if the sprite is on the ground
        if self.rect.bottom >= background.get_height():
            self.rect.bottom = background.get_height()
            self.on_ground = True
            self.y_velocity = 0
            self.is_jumping = False

        # Check if the sprite is over a blue pixel
        if self.is_over_blue_pixel():
            self.is_moving = False
            pygame.mixer.music.stop()  # Stop the audio

    def jump(self):
        if self.rect.top > 0:  # Continue jumping as long as the sprite hasn't reached the top
            self.y_velocity = self.jump_strength
            self.on_ground = False
            self.is_jumping = True
            self.has_jumped = True  # Mark that the sprite has jumped

    def stop_jumping(self):
        self.is_jumping = False  # Stop the upward movement

    def is_over_blue_pixel(self):
        # Get the color of the pixel where the sprite is
        pixel_x = int(self.rect.x + self.rect.width / 2)
        pixel_y = int(self.rect.y + self.rect.height / 2)

        if 0 <= pixel_x < background_rect.width and 0 <= pixel_y < background_rect.height:
            pixel_color = background.get_at((pixel_x, pixel_y))
            if pixel_y + 2 < background_rect.height:
                pixel_color_around = background.get_at((pixel_x, pixel_y + 2))
            elif pixel_y - 2 > background_rect.height: 
                pixel_color_around = background.get_at((pixel_x, pixel_y - 2))
            else:
                pixel_color_around = pixel_color
            # Check if the background pixel color is matplotlib-default blue 
            return pixel_color == (31, 119, 180, 255) and pixel_color_around == (31, 119, 180, 255)
        return False

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

    # Calculate the sprite speed in pixels per second
    screen_width = background.get_width()
    speed = screen_width / audio_length  # Pixels per second

    # Play the audio
    pygame.mixer.music.play()

    # Create a sprite group and add the moving sprite
    all_sprites = pygame.sprite.Group()
    sprite = MovingSprite(speed)
    all_sprites.add(sprite)

    clock = pygame.time.Clock()

    running = True
    while running:
        # Calculate the time passed since the last frame
        delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sprite.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    sprite.stop_jumping()
        
        # Update the sprite's position with the time-based approach
        all_sprites.update(delta_time)
        
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
background_rect = background.get_rect()

# Load the audio file
pygame.mixer.music.load('output.wav')
audio_length = pygame.mixer.Sound(audio_file).get_length()  # Duration in seconds

# Run the start screen
start_screen()

# Run the main game
main_game()