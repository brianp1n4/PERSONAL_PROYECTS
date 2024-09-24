import pygame
from character import cube
from enemy import Enemy
import random
from bullet import Bullet

pygame.init()

width = 1000
height = 800
window = pygame.display.set_mode ([width,height])
fps = 60
font = pygame.font.SysFont("Arial", 40)

playing = True
clock = pygame.time.Clock()
lifes = 5
score = 0
pass_time = 0
time_between_enemies = 500
cube = cube(width/2,height - 75)
enemies = []
bullets = []
last_bullet = 0
time_between_bullets = 500

enemies.append(Enemy(width/2,100))

def create_bullets():
    global last_bullet

    if pygame.time.get_ticks()-last_bullet > time_between_bullets:

        bullets.append(Bullet(cube.rect.centerx,cube.rect.centery))
        last_bullet = pygame.time.get_ticks()


def manage_keys(keys):
    # if keys[pygame.K_w]:
    #     cube.y -= cube.speed
    # if keys[pygame.K_s]:
    #     cube.y += cube.speed
    if keys[pygame.K_a]:
        cube.x -= cube.speed
    if keys[pygame.K_d]:
        cube.x += cube.speed
    if keys[pygame.K_SPACE]:        
        create_bullets()

while playing and lifes > 0:

    pass_time += clock.tick(fps)
    if pass_time > time_between_enemies:
        enemies.append(Enemy(random.randint(0,width),-100))
        pass_time = 0
        
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    lifes_display = font.render(f"Vidas: {lifes}", True, "white")
    score_display = font.render(f"Score: {score}", True, "white")

    manage_keys(keys)

    for event in events:
        if event.type == pygame.QUIT:
            playing = False

    window.fill("black")
    cube.draw(window)

    for enemy in enemies:
        enemy.draw(window)
        enemy.movement()

        if pygame.Rect.colliderect(cube.rect, enemy.rect):
            lifes -= 1
            print(f"Te quedan {lifes}")
            enemies.remove(enemy)
            # if lifes == 0:
            #     quit()

        if enemy.y + enemy.height > height:
            score += 1
            enemies.remove(enemy)   

        for bullet in bullets:
            if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                enemy.life -= 1
                bullets.remove(bullet)
                score += 1

        if enemy.life <= 0:
            enemy.remove(enemies)

        
    for bullet in bullets:
        bullet.draw(window)
        bullet.movement()

    window.blit(lifes_display,(20, 20))
    window.blit(score_display,(20, 60))

    pygame.display.update()

quit()
