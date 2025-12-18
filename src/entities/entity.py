# ==============================================================================
# ENTITY - CLASE BASE PARA TODAS LAS ENTIDADES DEL JUEGO
# ==============================================================================
# Esta clase base define la interfaz común para todas las entidades
# (jugador, enemigos, balas, power-ups, etc.)

import pygame
from abc import ABC, abstractmethod

class Entity(pygame.sprite.Sprite, ABC):
    """
    Clase base abstracta para todas las entidades del juego.
    
    Hereda de pygame.sprite.Sprite para aprovechar el sistema de sprites
    y de ABC (Abstract Base Class) para forzar la implementación de métodos.
    
    ¿Por qué heredar de Sprite?
    - Sistema de grupos automático (facilita colisiones)
    - Métodos update() y kill() integrados
    - Optimización de renderizado
    """
    
    def __init__(self, x, y, width, height):
        """
        Constructor base de todas las entidades.
        
        Args:
            x: Posición horizontal inicial (píxeles)
            y: Posición vertical inicial (píxeles)
            width: Ancho de la entidad (píxeles)
            height: Alto de la entidad (píxeles)
        """
        # Inicializar la clase padre Sprite
        super().__init__()
        
        # Crear la superficie (imagen) de la entidad
        # Por ahora usamos un rectángulo de color
        # Más adelante podemos reemplazar con sprites reales
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))  # Blanco por defecto
        
        # Obtener el rectángulo de la superficie
        # rect es fundamental para posicionamiento y colisiones
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Velocidad de la entidad (píxeles por frame)
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Estado de vida (para saber si debe ser eliminada)
        self.alive = True
    
    @abstractmethod
    def update(self, delta_time):
        """
        Actualiza la lógica de la entidad.
        
        ABSTRACTO: Cada entidad debe implementar su propia lógica.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        pass
    
    def draw(self, screen):
        """
        Dibuja la entidad en pantalla.
        
        Por defecto usa self.image y self.rect.
        Las subclases pueden sobrescribir este método para
        efectos visuales más complejos.
        
        Args:
            screen: Superficie donde dibujar
        """
        screen.blit(self.image, self.rect)
    
    def move(self, delta_time):
        """
        Mueve la entidad según su velocidad.
        
        Usa delta_time para movimiento independiente de FPS.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        self.rect.x += self.velocity_x * delta_time
        self.rect.y += self.velocity_y * delta_time
    
    def destroy(self):
        """
        Marca la entidad para destrucción.
        
        En el próximo update, será removida del juego.
        """
        self.alive = False
        self.kill()  # Método de Sprite que remueve de todos los grupos
