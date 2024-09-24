import pygame
import os

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.life = 5

        # Carga de la imagen con ruta relativa y manejo de errores
        current_dir = os.path.dirname(__file__)
        try:
            self.imagen = pygame.image.load(os.path.join(current_dir, "enemy2.png"))
            self.imagen = pygame.transform.scale(self.imagen, (self.width, self.height))
        except pygame.error as e:
            print(f"Error al cargar la imagen del enemigo: {e}")
            self.imagen = None  # Maneja este caso como mejor te convenga

    def draw(self, window):
        # Actualiza la posición del rectángulo
        self.rect.topleft = (self.x, self.y)

        # Solo dibuja la imagen si está cargada correctamente
        if self.imagen:
            window.blit(self.imagen, (self.x, self.y))
        # Si no hay imagen, podrías optar por dibujar un rectángulo
        # else:
        #     pygame.draw.rect(window, (0, 0, 0), self.rect)

    def movement(self):
        self.y += self.speed
        # Actualiza las coordenadas del rectángulo
        self.rect.topleft = (self.x, self.y)
