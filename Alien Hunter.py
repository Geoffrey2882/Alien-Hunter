import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
clock = pygame.time.Clock()
# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
LIFT_FORCE = 5
MISSILE_SPEED = 4
PLAYER_FIRE_RATE = 20

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Hunter")
# Load the background image
bg = pygame.image.load("Background.jpeg").convert()

# Load the death screen image
death_screen = pygame.image.load("DeathScreen.jpeg").convert()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("FighterPlane.png").convert()
        self.rect = self.image.get_rect()
        self.rect.left = 100  # Set the left position of the player
        self.rect.centery = SCREEN_HEIGHT // 2  # Center the player vertically
        self.velocity = 0  # Player's vertical velocity
        self.velocity2 = 0
        self.fire_counter = 0

    def update(self):
        # Update player's position based on velocity
        self.rect.y += self.velocity
        self.rect.x += self.velocity2
        # Keep the player within the screen bounds
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity2 = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.velocity2 = 0

        # Increment fire counter
        self.fire_counter += 1

    def descend(self):
        self.velocity = LIFT_FORCE
        self.image = pygame.image.load("FighterPlaneDown.png").convert_alpha()

    def lift(self):
        self.velocity = -LIFT_FORCE
        self.image = pygame.image.load("FighterPlaneUp.png").convert_alpha()

    def left(self):
        self.velocity2 = -LIFT_FORCE
        
    def right(self):
        self.velocity2 = LIFT_FORCE

    def stay(self):
        self.velocity, self.velocity2 = 0,0
        self.image = pygame.image.load("FighterPlane.png").convert_alpha()

    def shoot_missile(self):
        if self.fire_counter >= PLAYER_FIRE_RATE:
            # Create a new missile and add it to the sprite group
            pygame.mixer.music.load("Missile.mp3")
            pygame.mixer.music.play()
            missile = Missile(self.rect.right-20, self.rect.centery-10)
            all_sprites.add(missile)
            player_missiles.add(missile)
            self.fire_counter = 0

# UFO class
class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [pygame.image.load("UFO.png").convert_alpha(),
                       pygame.image.load("UFO2.png").convert_alpha()]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_WIDTH+200
        self.rect.centery = random.randint(100, SCREEN_HEIGHT - 100)
        self.velocity = UFO_SPEED
        self.fire_rate = UFO_FIRE_RATE
        self.fire_counter = 0

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.right = SCREEN_WIDTH
            self.rect.centery = random.randint(100, SCREEN_HEIGHT - 100)
            self.fire_counter = 0

        self.fire_counter += 1
        if self.fire_counter == self.fire_rate:
            self.fire_counter = 0
            self.shoot()

        # Update UFO image frames to alternate between UFO.png and UFO2.png
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]

    def shoot(self):
        # Create a new laser and add it to the sprite group
        pygame.mixer.music.load("Laser.mp3")
        pygame.mixer.music.play()
        laser = Laser(self.rect.left+20, self.rect.centery-10)
        all_sprites.add(laser)
        ufo_lasers.add(laser)

# Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Missile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y

    def update(self):
        self.rect.x *= 100 / 99
        self.rect.x += MISSILE_SPEED * 100 / 99
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y

    def update(self):
        self.rect.x -= (MISSILE_SPEED ** 3) / 2
        if self.rect.right < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
ufo_lasers = pygame.sprite.Group()
player_missiles = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create invisible barriers as the floor and ceiling
floor_barrier = pygame.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
ceiling_barrier = pygame.Rect(0, 0, SCREEN_WIDTH, 10)

# Score counter
score = 0
font = pygame.font.Font(None, 36)

# Death screen flag
is_dead = False

# Infinite scrolling background
bg_x = 0
bg_speed = 2

# Difficulty levels
EASY = {
    'ufo_fire_rate': 120,
    'chance': 200,
    'ufo_speed':3
}

NORMAL = {
    'ufo_fire_rate': 105,
    'chance': 150,
    'ufo_speed':4
}

UNFAIR = {
    'ufo_fire_rate': 90,
    'chance': 100,
    'ufo_speed':5
}

# Starting screen function
def start_screen():
    font_title = pygame.font.Font(None, 72)
    font_difficulty = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return EASY
                elif event.key == pygame.K_n:
                    return NORMAL
                elif event.key == pygame.K_u:
                    return UNFAIR

        screen.fill((0, 0, 0))
        title_text = font_title.render("Alien Hunter", True, (255, 255, 255))
        text = font_difficulty.render("Shoot as many UFOs as you can! Arrow Keys/WASD for Movement, SPACE to Shoot Missiles",True,(255,255,255))
        easy_text = font_difficulty.render("Press 'E' for Easy", True, (255, 255, 255))
        normal_text = font_difficulty.render("Press 'N' for Normal", True, (255, 255, 255))
        unfair_text = font_difficulty.render("Press 'U' for Unfair", True, (255, 255, 255))

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(normal_text, (SCREEN_WIDTH // 2 - normal_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(unfair_text, (SCREEN_WIDTH // 2 - unfair_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

        pygame.display.flip()
        clock.tick(60)

# Show the starting screen and get the selected difficulty level
selected_difficulty = start_screen()

# Set the difficulty settings based on the selected level
UFO_FIRE_RATE = selected_difficulty['ufo_fire_rate']
CHANCE = selected_difficulty['chance']
UFO_SPEED = selected_difficulty['ufo_speed']

# Starting screen function
def show_start_screen():
    screen.blit(bg, (bg_x, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Main game loop
game = True
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    CHANCE += 0.02
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.lift()
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.descend()
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.left()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.right()
    elif keys[pygame.K_SPACE]:
        player.shoot_missile()
    else:
        player.stay()

    if not is_dead:
        # Update
        all_sprites.update()

        # Check for collisions with UFO lasers
        hits = pygame.sprite.spritecollide(player, ufo_lasers, True)
        if hits:
            is_dead = True
        # Remove UFOs that go off the screen
        for ufo in ufo_group.copy():
            if ufo.rect.right < 0:
                ufo.kill()
                is_dead = True
        # Check for collisions between player missiles and UFOs
        ufo_hits = pygame.sprite.groupcollide(ufo_group, player_missiles, True, True)
        for ufo in ufo_hits:
            score += 1

        # Create new UFOs to fill in the space
        while len(ufo_group) < 3:
            new_ufo = UFO()
            ufo_group.add(new_ufo)
            all_sprites.add(new_ufo)

        # Infinite scrolling background
        bg_x -= bg_speed
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

    # Draw the background multiple times to create an infinite scrolling effect
    for i in range(2):
        screen.blit(bg, (bg_x + i * SCREEN_WIDTH, 0))

    if not is_dead:
        all_sprites.draw(screen)  # Draw all the sprites on top of the background
        pygame.draw.rect(screen, (0, 0, 0), floor_barrier)  # Draw the floor barrier for visualization
        pygame.draw.rect(screen, (0, 0, 0), ceiling_barrier)  # Draw the ceiling barrier for visualization
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
    else:
        screen.blit(death_screen, [0, 0])
        score_text = font.render("Final Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150))
        game = False

    pygame.display.flip()

    all_sprites.clear(screen, bg)  # Clear all the sprites from the previous frame
    clock.tick(60)
pygame.mixer.music.load("Death.mp3")
pygame.mixer.music.play()
while game == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
