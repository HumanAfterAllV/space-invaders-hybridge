# ==============================================================================
# PLAYER - JUGADOR
# ==============================================================================
# Clase que representa al jugador (la nave espacial)

import pygame
from src.entities.entity import Entity
from config import *

class Player(Entity):
    """
    Clase del jugador.
    
    Responsabilidades:
    - Movimiento horizontal con teclado
    - Disparo de balas
    - Gestión de vidas
    - Colisiones con enemigos/balas
    """
    
    def __init__(self, x, y):
        """
        Constructor del jugador.
        
        Args:
            x: Posición horizontal inicial
            y: Posición vertical inicial
        """
        # Llamar al constructor de Entity
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Cargar sprite del jugador desde imagen
        try:
            self.image = pygame.image.load('assets/images/player.png').convert_alpha()
            # Escalar la imagen al tamaño configurado
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            print("✅ Sprite del jugador cargado")
        except pygame.error as e:
            print(f"⚠️ No se pudo cargar sprite del jugador: {e}")
            # Fallback: usar rectángulo azul
            self.image.fill(BLUE)
        
        # Velocidad de movimiento (se usa cuando se presionan teclas)
        self.speed = PLAYER_SPEED
        
        # Cooldown de disparo
        self.shoot_cooldown = 0  # Tiempo restante hasta poder disparar
        self.shoot_delay = PLAYER_SHOOT_COOLDOWN / 1000.0  # Convertir ms a segundos
        
        # Vidas del jugador
        self.lives = PLAYER_LIVES
        
        # Estado de invulnerabilidad (después de ser golpeado)
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 2.0  # 2 segundos de invulnerabilidad
    
    def handle_input(self):
        """
        Maneja el input del teclado para mover al jugador.
        
        Controles:
        - A / FLECHA_IZQUIERDA: Mover a la izquierda
        - D / FLECHA_DERECHA: Mover a la derecha
        
        Nota: No usamos events, sino get_pressed() para
        movimiento continuo y suave.
        """
        # Obtener estado de todas las teclas
        # get_pressed() retorna un diccionario de teclas
        keys = pygame.key.get_pressed()
        
        # Resetear velocidad horizontal
        self.velocity_x = 0
        
        # Movimiento a la izquierda
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        
        # Movimiento a la derecha
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
    
    def update(self, delta_time):
        """
        Actualiza la lógica del jugador.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        # Manejar input del teclado
        self.handle_input()
        
        # Mover al jugador según su velocidad
        self.rect.x += self.velocity_x
        
        # Aplicar límites de pantalla (no puede salir)
        # Limitar por la izquierda
        if self.rect.left < 0:
            self.rect.left = 0
        
        # Limitar por la derecha
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        
        # Actualizar cooldown de disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= delta_time
        
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.invulnerable_time -= delta_time
            if self.invulnerable_time <= 0:
                self.invulnerable = False
    
    def can_shoot(self):
        """
        Verifica si el jugador puede disparar.
        
        Returns:
            bool: True si puede disparar, False si está en cooldown
        """
        return self.shoot_cooldown <= 0
    
    def shoot(self):
        """
        Dispara una bala (resetea el cooldown).
        
        Nota: Este método solo marca que se disparó.
        La creación de la bala se hace en GameScreen.
        
        Returns:
            tuple: Posición (x, y) desde donde sale la bala
        """
        if self.can_shoot():
            # Resetear cooldown
            self.shoot_cooldown = self.shoot_delay
            
            # Calcular posición de spawn de la bala
            # Sale del centro-arriba del jugador
            bullet_x = self.rect.centerx
            bullet_y = self.rect.top
            
            return (bullet_x, bullet_y)
        
        return None
    
    def take_damage(self):
        """
        El jugador recibe daño.
        
        Reduce una vida y activa invulnerabilidad temporal.
        """
        if not self.invulnerable:
            self.lives -= 1
            print(f"💔 Jugador golpeado! Vidas restantes: {self.lives}")
            
            if self.lives > 0:
                # Activar invulnerabilidad
                self.invulnerable = True
                self.invulnerable_time = self.invulnerable_duration
            else:
                # Game Over
                print("☠️ Game Over!")
                self.destroy()
    
    def draw(self, screen):
        """
        Dibuja al jugador.
        
        Si está invulnerable, parpadea (efecto visual).
        
        Args:
            screen: Superficie donde dibujar
        """
        # Si está invulnerable, hacer parpadeo
        if self.invulnerable:
            # Parpadear cada 0.1 segundos
            if int(self.invulnerable_time * 10) % 2 == 0:
                return  # No dibujar (efecto de parpadeo)
        
        # Dibujar normalmente
        super().draw(screen)
