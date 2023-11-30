import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fallSpeed = 0

    def update(self, gravity):
        self.fallSpeed += gravity
        self.rect.y += self.fallSpeed
        if self.rect.y > ScreenY - self.rect.height:
            self.rect.y = ScreenY - self.rect.height
            self.fallSpeed = 0

    def jump(self):
        if self.rect.y == ScreenY - self.rect.height:
            self.fallSpeed = jumpSpeed

class GreenBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

class FlyingSquare(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


# Initialize Pygame
pygame.init()

# Set up the screen
ScreenX = 800
ScreenY = 500
screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption('Jumping Square')

# Set up the player sprite
player = Player(200, ScreenY - 100, 25, 25)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set up the green block sprite group
green_blocks = pygame.sprite.Group()
flying_squares = pygame.sprite.Group()

# Set up the clock
clock = pygame.time.Clock()

# Game variables
gravity = 0.5
speed = 5
jumpSpeed = -10
running = True
spawn_frequency = 50
spawn_timer = spawn_frequency
score = 0

show_game_over = False

def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    text = font.render(f"You Died. Score: {score}. Press 'R' to restart.", True, (255, 0, 0))
    text_rect = text.get_rect(center=(ScreenX // 2, ScreenY // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not show_game_over:
                player.jump()
            elif event.key == pygame.K_r and show_game_over:
                # Restart the game
                show_game_over = False
                player.rect.x = 200
                player.rect.y = ScreenY - 100
                player.fallSpeed = 0
                for block in green_blocks:
                    block.kill()  # Kill each green block sprite
                for square in flying_squares:
                    square.kill()  # Kill each flying square sprite
                spawn_timer = spawn_frequency
                score = 0
            elif event.key == pygame.K_q:
                pygame.quit()

    if not show_game_over:
        score += 1
        all_sprites.update(gravity)
        green_blocks.update(speed)
        flying_squares.update()

        # Randomly spawn green blocks
        spawn_timer -= 1
        if spawn_timer <= 0:
            block_height = random.randint(20, min(70, ScreenY - 50))  # Adjusted maximum block height
            green_block = GreenBlock(ScreenX, ScreenY - block_height, 25, block_height)
            green_blocks.add(green_block)
            all_sprites.add(green_block)
            spawn_timer = spawn_frequency

        if random.randint(0, 200) == 0:  # Adjust the frequency of appearance
            flying_square = FlyingSquare(ScreenX, random.randint(ScreenY - 200, ScreenY - 80), 25, 25, 7)
            flying_squares.add(flying_square)
            all_sprites.add(flying_square)

        # Check for collisions between the player and green blocks
        if pygame.sprite.spritecollideany(player, green_blocks, pygame.sprite.collide_mask):
            show_game_over = True
        elif pygame.sprite.spritecollideany(player, flying_squares, pygame.sprite.collide_mask):
            show_game_over = True

    screen.fill((255, 255, 255))

    # Draw all sprites
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if show_game_over:
        show_game_over_screen()

    pygame.display.flip()

pygame.quit()