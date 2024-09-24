import pygame
import os

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 3
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        current_dir = os.path.dirname(__file__)  # Ruta relativa al directorio del script
        try:
            self.imagen = pygame.image.load(os.path.join(current_dir, "item.jpg"))
            self.imagen = pygame.transform.scale(self.imagen, (self.width, self.height))
        except pygame.error as e:
            print(f"Error al cargar la imagen: {e}")
            self.imagen = None  # Maneja el error como consideres necesario

    def draw(self, window):
        # Solo dibuja la imagen si está cargada
        if self.imagen:
            window.blit(self.imagen, (self.x, self.y))
        # Si no hay imagen, podrías optar por dibujar un rectángulo
        # else:
        #     pygame.draw.rect(window, (0, 0, 0), self.rect)

    def movement(self):
        self.y += self.speed
        # Actualiza las coordenadas del rectángulo
        self.rect.topleft = (self.x, self.y)
