import os
import random

import pygame
import pygame.math

pygame.font.init()
pygame.mixer.init()

# Making the main surface
# Height and Width we want the window to be inside of tuple
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsan', 100)

FPS = 60
velocity = 3
BULLET_VEL = 6
MAX_BULLETS = 5
bullet_damage = 1
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
POWERUP_SIZE = 25, 25
powerup_width = 25
powerup_height = 25

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Inserting the spaceships into the game and drawing them
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

POWER_UP_TYPES = ['Speed', 'Stronger_Bullets']


class PowerUp:
    def __init__(self, x, y, powerup_type, image_path):
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, POWERUP_SIZE)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def spawn_powerup():
    powerup_type = random.choice(POWER_UP_TYPES)
    image_path = os.path.join('Assets', 'Powerup.png')
    powerup = PowerUp(random.randint(0, WIDTH), random.randint(0, HEIGHT), powerup_type, image_path)
    return powerup


def handle_powerups(player_rect, powerups, player):
    player = RED_SPACESHIP, YELLOW_SPACESHIP
    for powerup in powerups:
        if player_rect.colliderect(pygame.Rect(powerup.x, powerup.y, powerup_width, powerup_height)):
            if powerup.powerup_type == 'Speed':
                if player == RED_SPACESHIP:
                    velocity += 1
                elif player == YELLOW_SPACESHIP:
                    velocity += 1
            elif powerup.powerup_type == 'Stronger_Bullets':
                if player == RED_SPACESHIP:
                    bullet_damage += 1
                elif player == YELLOW_SPACESHIP:
                    bullet_damage += 1
            powerups.remove(powerup)


def draw_powerups(powerups):
    for powerup in powerups:
        powerup.draw(WIN)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # Use blit to draw surface onto screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movment(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - velocity > 0:  # Left
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + velocity + yellow.width < BORDER.x:  # Right
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y - velocity > 0:  # Up
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + velocity + yellow.height < HEIGHT - 15:  # Down
        yellow.y += velocity


def red_handle_movment(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - velocity > BORDER.x + BORDER.width:  # Left
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + velocity + red.width < WIDTH:  # Right
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y - velocity > 0:  # Up
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + velocity + red.height < HEIGHT - 15:  # Down
        red.y += velocity


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


# Handles main pygame loop
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    powerups = []
    powerup_spawn_chance = 0.02
    # Clock controls the speed of the while loop per second
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # Getting all game events taking place inlcuding movement, collisions, etc.
        for event in pygame.event.get():
            # Ends while loop(quits the game)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movment(keys_pressed, yellow)
        red_handle_movment(keys_pressed, red)
        handle_powerups(yellow, powerups, YELLOW_SPACESHIP)
        handle_powerups(red, powerups, RED_SPACESHIP)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        if random.random() < powerup_spawn_chance:
            powerup = spawn_powerup()
            powerups.append(powerup)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        draw_powerups(powerups)

    main()


if __name__ == "__main__":
    main()
