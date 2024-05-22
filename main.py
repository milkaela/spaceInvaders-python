import math
import random
import pygame
from pygame import mixer

# Inițializarea Pygame
pygame.init()

# Dimensiuni ecran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader - Start Screen")


# Funcție pentru desenarea unui buton rotunjit
def draw_rounded_button(surface, color, rect, text, text_color, font, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# Funcție pentru ecranul de start
def start_screen():
    background_image = pygame.image.load('newbackground.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    screen.blit(background_image, (0, 0))

    title_font = pygame.font.Font('PixeloidMono-d94EV.ttf', 60)
    title_text = title_font.render("Space Invader", True, (255, 255, 255))
    title_text_rect = title_text.get_rect(center=(screen_width // 2, 200))
    screen.blit(title_text, title_text_rect)

    button_width = 200
    button_height = 80
    button_color = (100, 230, 255)
    text_color = (255, 255, 255)
    button_font = pygame.font.Font('PixeloidMono-d94EV.ttf', 28)
    button_text = button_font.render("Start Game", True, text_color)
    button_rect = pygame.Rect(screen_width // 2 - button_width // 2, 400, button_width, button_height)
    draw_rounded_button(screen, button_color, button_rect, "", text_color, button_font, 10)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False


start_screen()

# Inițializare variabile joc
background = pygame.image.load('newbackground.jpg')
mixer.music.load("backgroundSound.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.webp')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaceship.webp')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

initial_enemy_speed = 1.3  # Viteza inițială a inamicilor
max_enemy_speed = 3.1
speed_increase_interval = 15  # Secunde
speed_increase_amount = 0.3
last_speed_increase_time = pygame.time.get_ticks()

# Inițializare asteroizi
for i in range(num_of_enemies):
    asteroid_image = pygame.image.load('asteroid.png')
    asteroid_image.fill((180, 180, 180, 255), special_flags=pygame.BLEND_RGBA_MULT)
    enemyImg.append(asteroid_image)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(initial_enemy_speed)  # Viteză inițială
    enemyY_change.append(40)

# Așteptare scurtă pentru a evita ca asteroizii să pară lipiți între ei la începutul jocului
pygame.time.wait(1000)

bulletImg = pygame.image.load('newBullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('PixeloidMono-d94EV.ttf', 32)  # Folosim același font pentru toate textele și butoanele

textX = 10
textY = 10

over_font = pygame.font.Font('PixeloidMono-d94EV.ttf', 64)


# Funcție pentru afișarea scorului
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Funcție pentru afișarea textului de sfârșit de joc
def game_over_text():
    global highest_score
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(over_text, text_rect)

    # Afișare scor maxim
    show_highest_score(textX, textY + 50)

    # Actualizare scor maxim
    if score_value > highest_score:
        highest_score = score_value


# Funcție pentru afișarea jucătorului
def player(x, y):
    screen.blit(playerImg, (x, y))


# Funcție pentru afișarea inamicilor
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Funcție pentru tragererea unui glonț
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Funcție pentru verificarea coliziunii intre inamic si nava
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27


# Funcție pentru afișarea butonului de restart
def restart_button():
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_button_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(restart_text, restart_button_rect)
    return restart_button_rect


# Funcție pentru afișarea butonului de retry
def retry_button():
    retry_text = font.render("Retry", True, (255, 255, 255))
    retry_button_rect = retry_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(retry_text, retry_button_rect)
    return retry_button_rect


# Funcție pentru afișarea butonului de pauză
def pause_button():
    pause_text = font.render("Pause", True, (255, 255, 255))  # Afișăm doar un "P"
    pause_button_rect = pause_text.get_rect(topright=(screen_width - 10, 10))  # Poziționare dreapta sus
    screen.blit(pause_text, pause_button_rect)
    return pause_button_rect


highest_score = 0


# Funcție pentru afișarea scorului maxim
def show_highest_score(x, y):
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, (255, 255, 255))
    screen.blit(highest_score_text, (x, y))


# Funcție pentru afișarea butonului de resume (doar în modul pauză)
def resume_button():
    resume_text = font.render("Resume", True, (255, 255, 255))
    resume_button_rect = resume_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(resume_text, resume_button_rect)
    return resume_button_rect


# Funcție pentru afișarea mesajului de "Congratulations"
def congratulations_text():
    congrats_text1 = over_font.render("Congratulations!", True, (255, 255, 255))
    congrats_text2 = over_font.render("You won!", True, (255, 255, 255))
    text_rect1 = congrats_text1.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    text_rect2 = congrats_text2.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
    screen.blit(congrats_text1, text_rect1)
    screen.blit(congrats_text2, text_rect2)


running = True
game_over = False
congratulations = False
restart_rect = None
pause_rect = None
resume_rect = None
retry_rect = None
paused = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Verificăm dacă s-a dat clic pe butonul de pauză și nu suntem în ecranul de start
            if pause_rect and pause_rect.collidepoint(mouse_pos) and not game_over:
                paused = not paused
                if paused:
                    pygame.mixer.pause()
                    mixer.music.pause()
                else:
                    pygame.mixer.unpause()
                    mixer.music.unpause()
            # Verificăm dacă s-a dat clic pe butonul de resume (doar în modul pauză)
            elif paused and resume_rect and resume_rect.collidepoint(mouse_pos):
                paused = False
                pygame.mixer.unpause()
                mixer.music.unpause()
            # Verificăm dacă s-a dat clic pe butonul de retry (doar în ecranul de congratulații)
            elif congratulations and retry_rect and retry_rect.collidepoint(mouse_pos):
                congratulations = False
                score_value = 0
                playerX = 370
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                mixer.music.unpause()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("lasersound.wav")
                    bulletSound.set_volume(0.5)
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.pause()
                    mixer.music.pause()
                else:
                    pygame.mixer.unpause()
                    mixer.music.unpause()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not paused and not game_over and not congratulations:
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase_time > speed_increase_interval * 1000:
            last_speed_increase_time = current_time
            for i in range(num_of_enemies):
                enemyX_change[i] = min(enemyX_change[i] + speed_increase_amount, max_enemy_speed)

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over = True
                restart_rect = restart_button()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = abs(enemyX_change[i])  # Direcție dreapta
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -abs(enemyX_change[i])  # Direcție stânga
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosionEffect.wav")
                explosionSound.set_volume(0.5)
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                # Creștem viteza doar pentru asteroidul nou creat
                enemyX_change[i] = initial_enemy_speed + (score_value // 20) * 0.5

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

        if score_value >= 1:
            congratulations = True

    if game_over:
        game_over_text()
        restart_rect = restart_button()

    if not game_over and not congratulations:
        pause_rect = pause_button()
        if paused:
            resume_rect = resume_button()

    if congratulations:
        congratulations_text()
        retry_rect = retry_button()

    pygame.display.update()

    if game_over:
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and restart_rect and restart_rect.collidepoint(mouse_pos):
            game_over = False
            score_value = 0
            playerX = 370
            for i in range(num_of_enemies):
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
            mixer.music.unpause()

pygame.quit()
