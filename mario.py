import pygame
import sys

# --- CONSTANTS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('mario_stand.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 6
        self.jump_speed = -16
        self.on_ground = False
        
    def update(self, ground):
        keys = pygame.key.get_pressed()
        
        # 1. Horizontal Movement
        self.velocity_x = 0
        if keys[pygame.K_RIGHT]: self.velocity_x = self.speed
        if keys[pygame.K_LEFT]:  self.velocity_x = -self.speed
            
        self.rect.x += self.velocity_x
        
        # Check Horizontal Collision
        if self.rect.colliderect(ground.rect):
            if self.velocity_x > 0: self.rect.right = ground.rect.left
            if self.velocity_x < 0: self.rect.left = ground.rect.right

        # 2. Vertical Movement (Jumping & Gravity)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_speed
            
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False
        
        # Check Vertical Collision
        if self.rect.colliderect(ground.rect):
            if self.velocity_y > 0: # Falling and hitting the floor
                self.rect.bottom = ground.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0: # Jumping and hitting head
                self.rect.top = ground.rect.bottom
                self.velocity_y = 0

# --- SETUP ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Images
bg_image = pygame.image.load('background.png').convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

ground = pygame.sprite.Sprite()
ground.image = pygame.image.load('ground.png').convert_alpha()
ground.rect = ground.image.get_rect(bottomleft=(0, SCREEN_HEIGHT))

# Create Player
mario = Player(100, ground.rect.top)

# Group sprites for drawing
all_sprites = pygame.sprite.Group()
all_sprites.add(ground, mario)

# --- MAIN GAME LOOP ---
while True:
    
    # 1. Check for Quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # (Future logic: if game_ongoing == True: do the updates below)
            
    # 2. Update logic
    mario.update(ground)
    
    # 3. Draw Graphics
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)
    
    # 4. Refresh Screen
    pygame.display.update()
    clock.tick(FPS)