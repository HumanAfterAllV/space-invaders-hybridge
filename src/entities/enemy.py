# ==============================================================================
# ENEMY - ENEMIGO
# ==============================================================================
# Clase que representa a los enemigos (aliens)

import pygame
from src.entities.entity import Entity
from config import *

class Enemy(Entity):
    """
    Clase de los enemigos.
    
    Responsabilidades:
    - Movimiento en formación
    - Disparo aleatorio
    - Diferentes tipos (básico, rápido, tanque)
    - Animación de movimiento
    """
    
    def __init__(self, x, y, enemy_type="basic"):
        """
        Constructor del enemigo.
        
        Args:
            x: Posición horizontal inicial
            y: Posición vertical inicial
            enemy_type: Tipo de enemigo ("basic", "fast", "tank")
        """
        # Llamar al constructor de Entity
        super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        
        # Tipo de enemigo
        self.enemy_type = enemy_type
        
        # Cargar sprite del enemigo desde imagen
        try:
            self.image = pygame.image.load('assets/images/enemy.png').convert_alpha()
            # Escalar la imagen al tamaño configurado
            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
            
            # Aplicar tinte según el tipo de enemigo
            if enemy_type == "fast":
                # Enemigos rápidos: tinte cyan
                self.apply_tint((0, 255, 255, 100))  # Cyan
            elif enemy_type == "tank":
                # Enemigos tanque: tinte magenta
                self.apply_tint((255, 0, 255, 100))  # Magenta
            # "basic" mantiene el color original
            
            print(f"✅ Sprite de enemigo '{enemy_type}' cargado")
        except pygame.error as e:
            print(f"⚠️ No se pudo cargar sprite de enemigo: {e}")
            # Fallback: usar rectángulo de color según tipo
            if enemy_type == "basic":
                self.image.fill(CYAN)
            elif enemy_type == "fast":
                self.image.fill(YELLOW)
            elif enemy_type == "tank":
                self.image.fill(MAGENTA)
        
        # Configurar propiedades según el tipo
        if enemy_type == "basic":
            self.speed = ENEMY_SPEED
            self.health = 1
            self.points = SCORE_ENEMY_BASIC
        elif enemy_type == "fast":
            self.speed = ENEMY_SPEED * 2
            self.health = 1
            self.points = SCORE_ENEMY_FAST
        elif enemy_type == "tank":
            self.speed = ENEMY_SPEED * 0.5
            self.health = 3  # Requiere 3 disparos
            self.points = SCORE_ENEMY_TANK
        
        # Dirección de movimiento (1 = derecha, -1 = izquierda)
        self.direction = 1
        
        # Tiempo para el próximo disparo
        self.shoot_timer = 0
        self.shoot_cooldown = 2.0  # Dispara cada 2 segundos (aleatorio)
    
    def apply_tint(self, color):
        """
        Aplica un tinte de color a la imagen del enemigo.
        
        Args:
            color: Tupla RGBA (red, green, blue, alpha)
        """
        # Crear superficie de tinte
        tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        tint.fill(color)
        # Aplicar el tinte a la imagen
        self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    def update(self, delta_time):
        """
        Actualiza la lógica del enemigo.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        # Movimiento horizontal
        self.rect.x += self.speed * self.direction
        
        # Actualizar timer de disparo
        self.shoot_timer -= delta_time
    
    def move_down(self):
        """
        Mueve al enemigo hacia abajo (cuando llega al borde).
        """
        self.rect.y += ENEMY_DESCENT_SPEED
    
    def reverse_direction(self):
        """
        Invierte la dirección de movimiento horizontal.
        """
        self.direction *= -1
    
    def can_shoot(self):
        """
        Verifica si el enemigo puede disparar.
        
        Returns:
            bool: True si puede disparar, False si está en cooldown
        """
        return self.shoot_timer <= 0
    
    def shoot(self):
        """
        El enemigo dispara (resetea el timer).
        
        Returns:
            tuple: Posición (x, y) desde donde sale la bala, o None
        """
        if self.can_shoot():
            # Resetear timer con un valor aleatorio
            import random
            self.shoot_timer = random.uniform(1.0, 3.0)
            
            # Calcular posición de spawn de la bala
            # Sale del centro-abajo del enemigo
            bullet_x = self.rect.centerx
            bullet_y = self.rect.bottom
            
            return (bullet_x, bullet_y)
        
        return None
    
    def take_damage(self, damage=1):
        """
        El enemigo recibe daño.
        
        Args:
            damage: Cantidad de daño a recibir
        
        Returns:
            int: Puntos otorgados si murió, 0 si sigue vivo
        """
        self.health -= damage
        
        if self.health <= 0:
            # Enemigo muerto
            print(f"💥 Enemigo {self.enemy_type} destruido!")
            self.destroy()
            return self.points
        else:
            # Aún vivo (solo tanques pueden sobrevivir un disparo)
            print(f"🎯 Enemigo golpeado! Vida restante: {self.health}")
            # Efecto visual: parpadeo rojo (opcional)
            return 0
