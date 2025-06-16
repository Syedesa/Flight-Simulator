import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 320, 640
PLAYER_PLANE_SIZE = 50  # Adjusted size for the player plane
ENEMY_PLANE_SIZE = 50
BOSS_PLANE_SIZE = 100
BULLET_SIZE = 20

# Set up some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Load images
player_plane_image = pygame.image.load('player_plane.png')
player_plane_image = pygame.transform.scale(player_plane_image, (PLAYER_PLANE_SIZE, PLAYER_PLANE_SIZE))
enemy_plane_image = pygame.image.load('enemy_plane.png')
enemy_plane_image = pygame.transform.scale(enemy_plane_image, (ENEMY_PLANE_SIZE, ENEMY_PLANE_SIZE))
boss_plane_image = pygame.image.load('boss_plane.png')
boss_plane_image = pygame.transform.scale(boss_plane_image, (BOSS_PLANE_SIZE, BOSS_PLANE_SIZE))

background_image = pygame.image.load('space_background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

laser_bullet_image = pygame.image.load('laser_bullet.png')
laser_bullet_image = pygame.transform.scale(laser_bullet_image, (BULLET_SIZE, BULLET_SIZE))

retry_icon_image = pygame.image.load('retry_icon.png')
retry_icon_image = pygame.transform.scale(retry_icon_image, (50, 50))

# Load leaderboard from file
def load_leaderboard():
    try:
        with open("leaderboard.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

# Save leaderboard to file
def save_leaderboard(scores):
    with open("leaderboard.txt", "w") as f:
        f.write("\n".join(scores))

# Main menu
def main_menu():
    menu_items = ["Play", "Leaderboard", "Exit"]
    selected_item = 0

    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Draw title
        title_text = title_font.render("Airship Battle by Akif", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw menu items
        for i, item in enumerate(menu_items):
            color = WHITE if i == selected_item else (150, 150, 150)
            item_text = font.render(item, True, color)
            screen.blit(item_text, (50, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:  # Play
                        game_loop()
                    elif selected_item == 1:  # Leaderboard
                        show_leaderboard()
                    elif selected_item == 2:  # Exit
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 150 <= mouse_y <= 200:
                    game_loop()
                elif 200 <= mouse_y <= 250:
                    show_leaderboard()
                elif 250 <= mouse_y <= 300:
                    pygame.quit()
                    sys.exit()

# Show leaderboard
def show_leaderboard():
    scores = load_leaderboard()
    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        y = 50
        for score in scores:
            score_text = font.render(score, True, WHITE)
            screen.blit(score_text, (50, y))
            y += 30
        back_text = font.render("Press ESC to go back", True, WHITE)
        screen.blit(back_text, (50, HEIGHT - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Ask for player's name
def get_player_name(score):
    player_name = ""
    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        name_text = font.render("Enter your name:", True, WHITE)
        screen.blit(name_text, (50, HEIGHT // 2 - 50))

        name_display = font.render(player_name, True, WHITE)
        screen.blit(name_display, (50, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        scores = load_leaderboard()
                        scores.append(f"{player_name}: {score}")
                        save_leaderboard(scores)
                        return
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_SPACE:
                    player_name += ' '
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    player_name += chr(event.key)
                elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    player_name += chr(event.key)

# Game loop
def game_loop():
    player_plane = pygame.Rect(WIDTH / 2 - PLAYER_PLANE_SIZE / 2, HEIGHT - PLAYER_PLANE_SIZE - 20, PLAYER_PLANE_SIZE, PLAYER_PLANE_SIZE)
    enemy_planes = []
    bullets = []
    score = 0
    boss_plane = None
    boss_health = 0
    next_boss_score = 100
    game_over = False

    # Game settings
    enemy_speed = 2
    bullet_speed = 5
    boss_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        bullet = pygame.Rect(player_plane.centerx - BULLET_SIZE / 2, player_plane.top - BULLET_SIZE, BULLET_SIZE, BULLET_SIZE)
                        bullets.append(bullet)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_plane.x -= 5
        if keys[pygame.K_RIGHT]:
            player_plane.x += 5

        # Keep player plane within bounds
        player_plane.x = max(0, min(WIDTH - PLAYER_PLANE_SIZE, player_plane.x))

        # Add new enemy planes randomly
        if random.randint(1, 20) == 1:
            enemy_plane = pygame.Rect(random.randint(0, WIDTH - ENEMY_PLANE_SIZE), -ENEMY_PLANE_SIZE, ENEMY_PLANE_SIZE, ENEMY_PLANE_SIZE)
            enemy_planes.append(enemy_plane)

        # Update enemy planes
        for enemy_plane in enemy_planes:
            enemy_plane.y += enemy_speed
            if enemy_plane.y > HEIGHT:
                enemy_planes.remove(enemy_plane)
                score -= 10

        # Update bullets
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Check for collisions
        for enemy_plane in enemy_planes:
            if player_plane.colliderect(enemy_plane):
                game_over = True
                break
            for bullet in bullets:
                if bullet.colliderect(enemy_plane):
                    enemy_planes.remove(enemy_plane)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Check for boss plane
        if score >= next_boss_score and not boss_plane:
            boss_plane = pygame.Rect(WIDTH / 2 - BOSS_PLANE_SIZE / 2, -BOSS_PLANE_SIZE, BOSS_PLANE_SIZE, BOSS_PLANE_SIZE)
            boss_health = 10
            next_boss_score += 150

        if boss_plane:
            boss_plane.y += boss_speed
            if boss_plane.y > HEIGHT:
                boss_plane = None
                boss_health = 0

        # Update bullets
        for bullet in bullets:
            if boss_plane and bullet.colliderect(boss_plane):
                boss_health -= 1
                bullets.remove(bullet)
                if boss_health <= 0:
                    boss_plane = None
                    score += 50  # Bonus score for destroying boss
                    break

        # Draw everything
        screen.blit(background_image, (0, 0))
        screen.blit(player_plane_image, player_plane.topleft)
        for enemy_plane in enemy_planes:
            screen.blit(enemy_plane_image, enemy_plane.topleft)
        for bullet in bullets:
            screen.blit(laser_bullet_image, bullet.topleft)
        if boss_plane:
            screen.blit(boss_plane_image, boss_plane.topleft)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display game over message and retry icon
        if game_over:
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(retry_icon_image, (WIDTH // 2 - 25, HEIGHT // 2 + 10))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            get_player_name(score)
                            return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if WIDTH // 2 - 25 <= mouse_x <= WIDTH // 2 + 25 and HEIGHT // 2 + 10 <= mouse_y <= HEIGHT // 2 + 60:
                            get_player_name(score)
                            return

        pygame.display.flip()
        pygame.time.delay(30)

# Run the game
main_menu()
