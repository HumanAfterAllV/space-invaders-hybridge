# ==============================================================================
# BULLET - PROYECTIL
# ==============================================================================
# Clase que representa las balas disparadas por el jugador o enemigos

import pygame
from src.entities.entity import Entity
from config import *

class Bullet(Entity):
    """
    Clase de las balas/proyectiles.
    
    Características:
    - Movimiento vertical (arriba o abajo)
    - Auto-destrucción al salir de pantalla
    - Diferenciación entre bala del jugador y del enemigo
    """
    
    def __init__(self, x, y, direction, is_player_bullet=True):
        """
        Constructor de la bala.
        
        Args:
            x: Posición horizontal inicial
            y: Posición vertical inicial
            direction: 1 para arriba, -1 para abajo
            is_player_bullet: True si es del jugador, False si es del enemigo
        """
        # Llamar al constructor de Entity
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        
        # Cargar sprite de la bala desde imagen
        try:
            self.image = pygame.image.load('assets/images/bullet.png').convert_alpha()
            # Escalar la imagen al tamaño configurado
            self.image = pygame.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT))
            
            # Si es bala de enemigo, cambiar color (tintear de rojo)
            if not is_player_bullet:
                # Crear una copia para aplicar tinte rojo
                self.image = self.image.copy()
                red_tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                red_tint.fill((255, 0, 0, 128))  # Rojo semi-transparente
                self.image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        except pygame.error as e:
            print(f"⚠️ No se pudo cargar sprite de bala: {e}")
            # Fallback: usar rectángulo de color
            if is_player_bullet:
                self.image.fill(BULLET_COLOR)  # Amarillo para jugador
            else:
                self.image.fill(ENEMY_BULLET_COLOR)  # Rojo para enemigos
        
        # Velocidad vertical
        # direction: 1 = hacia arriba, -1 = hacia abajo
        # Multiplicamos por la velocidad configurada
        self.velocity_y = -BULLET_SPEED * direction
        
        # Guardar si es del jugador (útil para colisiones)
        self.is_player_bullet = is_player_bullet
        
        # Centrar la bala horizontalmente
        self.rect.centerx = x
        self.rect.centery = y
    
    def update(self, delta_time):
        """
        Actualiza la posición de la bala.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        # Mover la bala verticalmente
        self.rect.y += self.velocity_y
        
        # Auto-destruirse si sale de la pantalla
        # Bala del jugador: sale por arriba
        if self.is_player_bullet and self.rect.bottom < 0:
            self.destroy()
        
        # Bala del enemigo: sale por abajo
        elif not self.is_player_bullet and self.rect.top > WINDOW_HEIGHT:
            self.destroy()
