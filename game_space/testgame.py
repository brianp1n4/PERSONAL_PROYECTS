import pygame
from character import Cube
from enemy import Enemy
import random
from bullet import Bullet
from item import Item
import os

pygame.init()
pygame.mixer.init()
current_dir = os.path.dirname(__file__)

width = 1000
height = 800
window = pygame.display.set_mode([width, height])
fps = 60
font = pygame.font.SysFont("Arial", 40)

bullet_sfx_path = os.path.join(current_dir, "bullet_sfx.mp3")
enemy_death_sfx_path = os.path.join(current_dir, "enemy_death_sfx.mp3")

bullet_sfx = pygame.mixer.Sound(bullet_sfx_path)
enemy_death_sfx = pygame.mixer.Sound(enemy_death_sfx_path)

playing = True
clock = pygame.time.Clock()
lifes = 5
score = 0
pass_time = 0
time_between_enemies = 500
cube = Cube(width / 2, height - 75)
enemies = []
bullets = []
items = []
last_bullet = 0
time_between_bullets = 250
pass_time_items = 0
time_between_items = 3000

enemies.append(Enemy(width / 2, 100))
items.append(Item(width / 3, 100))

def create_bullets():
    global last_bullet
    if pygame.time.get_ticks() - last_bullet > time_between_bullets:
        bullets.append(Bullet(cube.rect.centerx, cube.rect.centery))
        last_bullet = pygame.time.get_ticks()
        bullet_sfx.play()

def manage_keys(keys):
    # Limitar los movimientos del cube para que no salga de la pantalla
    if keys[pygame.K_a] and cube.x - cube.speed >= 0:
        cube.x -= cube.speed
    if keys[pygame.K_d] and cube.x + cube.width + cube.speed <= width:
        cube.x += cube.speed
    if keys[pygame.K_w] and cube.y - cube.speed >= 0:
        cube.y -= cube.speed
    if keys[pygame.K_s] and cube.y + cube.height + cube.speed <= height:
        cube.y += cube.speed
    if keys[pygame.K_SPACE]:
        create_bullets()

while playing and lifes > 0:
    pass_time += clock.tick(fps)
    pass_time_items += clock.get_rawtime()

    if pass_time > time_between_enemies:
        enemies.append(Enemy(random.randint(0, width), -100))
        pass_time = 0

    if pass_time_items > time_between_items:
        items.append(Item(random.randint(0, width), -100))
        pass_time_items = 0

    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    lifes_display = font.render(f"Vidas: {lifes}", True, (255, 255, 255))
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))

    manage_keys(keys)

    for event in events:
        if event.type == pygame.QUIT:
            playing = False

    window.fill((0, 0, 0))
    cube.draw(window)

    enemies_to_remove = []
    bullets_to_remove = []

    for enemy in enemies:
        enemy.draw(window)
        enemy.movement()

        if pygame.Rect.colliderect(cube.rect, enemy.rect):
            lifes -= 1
            enemies_to_remove.append(enemy)

        for bullet in bullets:
            if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                enemy.life -= 1
                bullets_to_remove.append(bullet)
                score += 1

        if enemy.life <= 0:
            enemies_to_remove.append(enemy)
            enemy_death_sfx.play()

    for item in items:
        item.draw(window)            
        item.movement()

        if pygame.Rect.colliderect(item.rect, cube.rect):
            items.remove(item)
            # Asegurarse de no bajar el tiempo más allá de un límite
            if time_between_bullets > 100:
                time_between_bullets -= 50

    # Remover enemigos y balas fuera del bucle de iteración
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for bullet in bullets:
        bullet.draw(window)
        bullet.movement()

        if bullet.y < 0:
            bullets.remove(bullet)

    window.blit(lifes_display, (20, 20))
    window.blit(score_display, (20, 60))

    pygame.display.update()

pygame.quit()

name = input("Ingresa tu nombre: ")

with open('score.txt', 'a') as file:
    file.write(f"{name} - {score}\n")
