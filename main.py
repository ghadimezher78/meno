import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meno")

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Load and scale background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load and scale player image
player_image = pygame.image.load("player.png")
player_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))
player_speed = 5

# Load and scale enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_size = 50
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

# Load and scale fast enemy image
fast_enemy_image = pygame.image.load("fast_enemy.png")
fast_enemy_size = 40
fast_enemy_image = pygame.transform.scale(fast_enemy_image, (fast_enemy_size, fast_enemy_size))

def create_enemy(type="normal"):
    if type == "fast":
        x = random.randint(0, WIDTH - fast_enemy_size)
        y = random.randint(0, HEIGHT - fast_enemy_size)
        speed = [random.choice([-5, 5]), random.choice([-5, 5])]  # Fast speed
        health = 25  # Lower health
        return {"rect": pygame.Rect(x, y, fast_enemy_size, fast_enemy_size), "speed": speed, "health": health, "type": type}
    else:
        x = random.randint(0, WIDTH - enemy_size)
        y = random.randint(0, HEIGHT - enemy_size)
        speed = [random.choice([-2, 2]), random.choice([-2, 2])]
        health = 50
        return {"rect": pygame.Rect(x, y, enemy_size, enemy_size), "speed": speed, "health": health, "type": type}

# List of enemies
enemies = []

# Load and scale bullet image
bullet_image = pygame.image.load("bullet.png")
bullet_size = 20
bullet_image = pygame.transform.scale(bullet_image, (bullet_size, bullet_size))
bullet_speed = 10
bullets = []

# Load and scale obstacle image
obstacle_image = pygame.image.load("obstacle.png")
obstacle_size = (100, 100)  # Width and height of the obstacle
obstacle_image = pygame.transform.scale(obstacle_image, obstacle_size)

# Obstacles (example: a list of dicts with rect and image)
obstacles = [
    {"rect": pygame.Rect(300, 300, obstacle_size[0], obstacle_size[1]), "image": obstacle_image},
    {"rect": pygame.Rect(500, 100, obstacle_size[0], obstacle_size[1]), "image": obstacle_image}
]

# Load and scale power-up images
health_pack_image = pygame.image.load("health_pack.png")
health_pack_image = pygame.transform.scale(health_pack_image, (30, 30))
fire_rate_boost_image = pygame.image.load("fire_rate_boost.png")
fire_rate_boost_image = pygame.transform.scale(fire_rate_boost_image, (30, 30))

# Power-ups
power_ups = []

def create_power_up():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(0, HEIGHT - 30)
    type = random.choice(["health_pack", "fire_rate_boost"])
    return {"rect": pygame.Rect(x, y, 30, 30), "type": type}

# Respawn timer
RESPAWN_TIME = 3000  # 3 seconds
last_respawn_time = pygame.time.get_ticks()

# Score and high score
score = 0
high_score = 0
high_score_file = "high_score.txt"

# Load the high score from a file if it exists
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read())

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as f:
            f.write(str(high_score))

def show_game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        retry_text = font.render("Press 'R' to Retry", True, WHITE)
        quit_text = font.render("Press 'Q' to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(30)

def show_menu_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "start"
                elif event.key == pygame.K_i:
                    show_instructions_screen()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        title_text = large_font.render("Meno", True, WHITE)
        start_text = font.render("Press 'S' to Start", True, WHITE)
        instructions_text = font.render("Press 'I' for Instructions", True, WHITE)
        quit_text = font.render("Press 'Q' to Quit", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 200))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(30)

def show_instructions_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return

        screen.fill(BLACK)
        instructions_text = font.render("Use arrow keys to move.", True, WHITE)
        shoot_text = font.render("Press SPACE to shoot.", True, WHITE)
        power_up_text = font.render("Collect power-ups for benefits.", True, WHITE)
        back_text = font.render("Press 'B' to go back.", True, WHITE)
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(shoot_text, (WIDTH // 2 - shoot_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(power_up_text, (WIDTH // 2 - power_up_text.get_width() // 2, HEIGHT // 2))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(30)

def show_pause_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        pause_text = font.render("Game Paused", True, WHITE)
        resume_text = font.render("Press 'P' to Resume", True, WHITE)
        quit_text = font.render("Press 'Q' to Quit", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(30)

def reset_game():
    global player_pos, player_health, score, wave, enemies, bullets, power_ups, enemies_spawned, fire_rate
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_health = 100
    score = 0
    wave = 1
    enemies = []
    bullets = []
    power_ups = []
    enemies_spawned = False
    fire_rate = 500  # Milliseconds between shots
    spawn_wave(wave)

def spawn_wave(wave):
    global enemies_spawned
    num_enemies = wave * 5
    num_fast_enemies = wave * 2  # Increase number of fast enemies with each wave
    for _ in range(num_enemies):
        enemies.append(create_enemy())
    for _ in range(num_fast_enemies):
        enemies.append(create_enemy(type="fast"))
    enemies_spawned = True

def game_loop():
    global score, last_respawn_time, running, player_health, wave, enemies_spawned, fire_rate
    last_shot_time = pygame.time.get_ticks()
    power_up_spawn_time = pygame.time.get_ticks()
    power_up_duration = 5000  # 5 seconds duration for power-ups

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    show_pause_screen()
                elif event.key == pygame.K_SPACE:
                    if current_time - last_shot_time >= fire_rate:
                        # Create a new bullet
                        bullet_rect = pygame.Rect(player_pos[0] + player_size // 2 - bullet_size // 2,
                                                  player_pos[1], bullet_size, bullet_size)
                        bullets.append(bullet_rect)
                        last_shot_time = current_time

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Player rect for collision detection
        player_rect = pygame.Rect(*player_pos, player_size, player_size)

        # Check player collisions with obstacles
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle["rect"]):
                if keys[pygame.K_LEFT]:
                    player_pos[0] += player_speed
                if keys[pygame.K_RIGHT]:
                    player_pos[0] -= player_speed
                if keys[pygame.K_UP]:
                    player_pos[1] += player_speed
                if keys[pygame.K_DOWN]:
                    player_pos[1] -= player_speed

        # Move enemies
        for enemy in enemies:
            enemy["rect"].x += enemy["speed"][0]
            enemy["rect"].y += enemy["speed"][1]

            # Check for collision with obstacles
            for obstacle in obstacles:
                if enemy["rect"].colliderect(obstacle["rect"]):
                    enemy["speed"][0] = -enemy["speed"][0]
                    enemy["speed"][1] = -enemy["speed"][1]
                    break

            # Check for collision with walls
            if enemy["rect"].left < 0 or enemy["rect"].right > WIDTH:
                enemy["speed"][0] = -enemy["speed"][0]
            if enemy["rect"].top < 0 or enemy["rect"].bottom > HEIGHT:
                enemy["speed"][1] = -enemy["speed"][1]

            # Check for collision with player
            if player_rect.colliderect(enemy["rect"]):
                player_health -= 1
                if player_health <= 0:
                    save_high_score(score)
                    if show_game_over_screen() == "retry":
                        reset_game()
                        continue
                    else:
                        running = False

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Check for bullet collisions with enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy["rect"]):
                    bullets.remove(bullet)
                    enemy["health"] -= 25
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        score += 1
                    break

        # Check if all enemies are defeated to spawn the next wave
        if not enemies and enemies_spawned:
            wave += 1
            enemies_spawned = False
            spawn_wave(wave)

        # Check for collisions with power-ups
        for power_up in power_ups[:]:
            if player_rect.colliderect(power_up["rect"]):
                if power_up["type"] == "health_pack":
                    player_health = min(100, player_health + 25)
                elif power_up["type"] == "fire_rate_boost":
                    fire_rate = 200
                    power_up_spawn_time = current_time
                power_ups.remove(power_up)

        # Reset fire rate boost after duration ends
        if current_time - power_up_spawn_time > power_up_duration and fire_rate == 200:
            fire_rate = 500

        # Spawn power-ups at intervals
        if current_time - power_up_spawn_time > 10000:  # 10 seconds between power-up spawns
            power_ups.append(create_power_up())
            power_up_spawn_time = current_time

        # Draw the background
        screen.blit(background, (0, 0))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle["image"], (obstacle["rect"].x, obstacle["rect"].y))

        # Draw enemies
        for enemy in enemies:
            if enemy["type"] == "fast":
                screen.blit(fast_enemy_image, (enemy["rect"].x, enemy["rect"].y))
            else:
                screen.blit(enemy_image, (enemy["rect"].x, enemy["rect"].y))

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_image, (bullet.x, bullet.y))

        # Draw the player
        screen.blit(player_image, (player_rect.x, player_rect.y))

        # Draw power-ups
        for power_up in power_ups:
            if power_up["type"] == "health_pack":
                screen.blit(health_pack_image, (power_up["rect"].x, power_up["rect"].y))
            elif power_up["type"] == "fire_rate_boost":
                screen.blit(fire_rate_boost_image, (power_up["rect"].x, power_up["rect"].y))

        # Draw player health
        health_text = font.render("Health: {}".format(player_health), True, WHITE)
        screen.blit(health_text, (10, 10))

        # Draw score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

        # Draw high score
        high_score_text = font.render("High Score: {}".format(high_score), True, WHITE)
        screen.blit(high_score_text, (WIDTH - 150, 50))

        # Draw current wave
        wave_text = font.render("Wave: {}".format(wave), True, WHITE)
        screen.blit(wave_text, (WIDTH // 2 - wave_text.get_width() // 2, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

# Main game loop
running = True

# Show the menu screen first
while True:
    menu_choice = show_menu_screen()
    if menu_choice == "start":
        reset_game()
        game_loop()
    elif menu_choice == "quit":
        break
