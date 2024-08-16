import pygame

# Define the Sprite class with jumping capability
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, speed, background):
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

        # Track precise x position
        self.precise_x = self.rect.x

        # Fixed bounce velocity
        self.bounce_velocity_ground = 6
        self.bounce_velocity_top = 2

        # Background variables
        self.background = background
        self.background_rect = background.get_rect()

    def update(self, delta_time):
        if self.is_moving:
            # Update the precise x position
            self.precise_x += self.speed * delta_time

            # Update the rect.x to match the precise position
            self.rect.x = int(self.precise_x)

            # Stop the sprite if it reaches the right edge of the screen
            if self.rect.right >= self.background.get_width():
                self.rect.right = self.background.get_width()
                self.is_moving = False
                return "win"  # Return "win" to indicate the player won

        # Apply gravity if the sprite has jumped at least once and is not on the ground
        if self.has_jumped and not self.is_jumping:
            self.y_velocity += self.gravity

        # Update the vertical position
        self.rect.y += self.y_velocity

        # Check if the sprite hits the top of the screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y_velocity = self.bounce_velocity_top  # Fixed downward bounce velocity

        # Check if the sprite hits the ground
        if self.rect.bottom >= self.background.get_height():
            self.rect.bottom = self.background.get_height()
            self.y_velocity = -self.bounce_velocity_ground  # Fixed upward bounce velocity
            self.on_ground = True
            self.is_jumping = False

        # Check if the sprite is over a blue pixel
        if self.is_over_blue_pixel():
            self.is_moving = False
            pygame.mixer.music.stop()  # Stop the audio
            return "game_over"  # Return "game_over" to indicate the game over
        return None  # Return None if neither win nor game over

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

        if 0 <= pixel_x < self.background_rect.width and 0 <= pixel_y < self.background_rect.height:
            pixel_color = self.background.get_at((pixel_x, pixel_y))
            if pixel_y + 2 < self.background_rect.height:
                pixel_color_around = self.background.get_at((pixel_x, pixel_y + 2))
            elif pixel_y - 2 > self.background_rect.height: 
                pixel_color_around = self.background.get_at((pixel_x, pixel_y - 2))
            else:
                pixel_color_around = pixel_color
            # Check if the background pixel color is matplotlib-default blue 
            return pixel_color == (31, 119, 180, 255) and pixel_color_around == (31, 119, 180, 255)
        return False
