import pygame

# Load the sound wave image for the background
background = pygame.image.load('sound_wave.png')
background_rect = background.get_rect()

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
            return True  # Return True to indicate game over
        return False  # Return False if not game over

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
