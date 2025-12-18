# ==============================================================================
# GAME SCREEN - PANTALLA PRINCIPAL DEL JUEGO
# ==============================================================================
# Este estado es donde ocurre el juego real

import pygame
from src.screens.game_state import GameState
from src.entities import Player, Bullet
from config import *

class GameScreen(GameState):
    """
    Pantalla principal del juego.
    
    Responsabilidades:
    - Gestionar todas las entidades (jugador, enemigos, balas)
    - Detectar colisiones
    - Actualizar HUD (puntuación, vidas)
    - Detectar condiciones de victoria/derrota
    """
    
    def __init__(self, game):
        """
        Constructor de la pantalla de juego.
        
        Args:
            game: Referencia a la instancia principal del juego
        """
        super().__init__(game)
        
        # ========== GRUPOS DE SPRITES ==========
        # Los grupos facilitan actualizar/dibujar múltiples entidades
        # y detectar colisiones de forma eficiente
        
        # Grupo con TODAS las entidades (para update/draw global)
        self.all_sprites = pygame.sprite.Group()
        
        # Grupos específicos (para colisiones y lógica)
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()  # Solo balas del jugador
        self.enemy_bullets = pygame.sprite.Group()   # Solo balas de enemigos
        self.enemies = pygame.sprite.Group()
        
        # ========== ENTIDADES ==========
        self.player = None  # Se crea en enter()
        
        # ========== JUEGO STATE ==========
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        
        # ========== UI ==========
        self.font_hud = None
        self.font_game_over = None
    
    def enter(self):
        """
        Inicialización al entrar a la pantalla de juego.
        """
        print("🎬 Entrando a Game Screen")
        
        # Inicializar fuentes
        self.font_hud = pygame.font.SysFont('arial', 24)
        self.font_game_over = pygame.font.SysFont('arial', 64, bold=True)
        
        # Crear jugador
        # Posición: centro horizontal, cerca del fondo
        player_x = WINDOW_WIDTH // 2
        player_y = WINDOW_HEIGHT - 100
        self.player = Player(player_x, player_y)
        
        # Agregar jugador a los grupos
        self.all_sprites.add(self.player)
        self.players.add(self.player)
        
        # Resetear estado del juego
        self.score = 0
        self.game_over = False
        self.paused = False
        
        print("✅ Jugador creado en posición inicial")
        print("🎮 Controles: A/D o ←/→ para mover, SPACE para disparar")
    
    def handle_events(self, events):
        """
        Maneja eventos específicos del juego.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                
                # DISPARAR con SPACE
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player_shoot()
                
                # PAUSA con P
                elif event.key == pygame.K_p:
                    self.toggle_pause()
                
                # REINICIAR con R (si es game over)
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def player_shoot(self):
        """
        El jugador intenta disparar.
        
        Crea una bala si el cooldown lo permite.
        """
        # Intentar disparar
        bullet_pos = self.player.shoot()
        
        # Si puede disparar (no está en cooldown)
        if bullet_pos is not None:
            # Crear nueva bala
            bullet = Bullet(
                bullet_pos[0],  # x
                bullet_pos[1],  # y
                direction=1,    # Hacia arriba
                is_player_bullet=True
            )
            
            # Agregar a los grupos
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.player_bullets.add(bullet)
            
            print("🔫 ¡Bala disparada!")
            # TODO: Reproducir sonido de disparo
    
    def toggle_pause(self):
        """
        Alterna entre pausa y juego activo.
        """
        self.paused = not self.paused
        if self.paused:
            print("⏸️ Juego pausado")
        else:
            print("▶️ Juego reanudado")
    
    def restart_game(self):
        """
        Reinicia el juego (vuelve a enter()).
        """
        print("🔄 Reiniciando juego...")
        
        # Limpiar todos los sprites
        self.all_sprites.empty()
        self.players.empty()
        self.bullets.empty()
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        
        # Volver a inicializar
        self.enter()
    
    def update(self, delta_time):
        """
        Actualiza la lógica del juego.
        
        Args:
            delta_time: Tiempo desde el último frame (segundos)
        """
        # No actualizar si está pausado o game over
        if self.paused or self.game_over:
            return
        
        # Actualizar todas las entidades
        # Cada sprite ejecuta su método update()
        for sprite in self.all_sprites:
            sprite.update(delta_time)
        
        # TODO: Detectar colisiones
        # self.check_collisions()
        
        # Verificar si el jugador murió
        if self.player.lives <= 0:
            self.game_over = True
            print("☠️ GAME OVER!")
    
    def draw(self):
        """
        Dibuja la pantalla de juego.
        """
        # Limpiar pantalla (fondo negro del espacio)
        self.screen.fill(BLACK)
        
        # TODO: Dibujar fondo de estrellas
        
        # Dibujar todas las entidades
        for sprite in self.all_sprites:
            sprite.draw(self.screen)
        
        # Dibujar HUD (puntuación, vidas)
        self.draw_hud()
        
        # Si está pausado, mostrar mensaje
        if self.paused:
            self.draw_pause_menu()
        
        # Si es game over, mostrar mensaje
        if self.game_over:
            self.draw_game_over()
    
    def draw_hud(self):
        """
        Dibuja el HUD (Head-Up Display): puntuación, vidas, nivel.
        """
        # Margen desde el borde
        margin = 10
        
        # Puntuación (arriba izquierda)
        score_text = self.font_hud.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (margin, margin))
        
        # Vidas (arriba derecha)
        lives_text = self.font_hud.render(f"LIVES: {self.player.lives}", True, GREEN)
        lives_rect = lives_text.get_rect(topright=(WINDOW_WIDTH - margin, margin))
        self.screen.blit(lives_text, lives_rect)
        
        # Nivel (arriba centro)
        level_text = self.font_hud.render(f"LEVEL {self.level}", True, CYAN)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, margin))
        self.screen.blit(level_text, level_rect)
    
    def draw_pause_menu(self):
        """
        Dibuja el menú de pausa.
        """
        # Overlay semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)  # Semi-transparente
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto "PAUSED"
        pause_text = self.font_game_over.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instrucción
        instruction = self.font_hud.render("Press P to resume", True, WHITE)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_over(self):
        """
        Dibuja la pantalla de Game Over.
        """
        # Overlay semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto "GAME OVER"
        game_over_text = self.font_game_over.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Puntuación final
        final_score = self.font_hud.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = final_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(final_score, score_rect)
        
        # Instrucciones
        restart_text = self.font_hud.render("Press R to restart", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_hud.render("Press ESC for menu", True, GRAY)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
        self.screen.blit(menu_text, menu_rect)
    
    def exit(self):
        """
        Limpieza al salir de la pantalla de juego.
        """
        print("🚪 Saliendo de Game Screen")
        
        # Limpiar todos los sprites
        self.all_sprites.empty()
        self.players.empty()
        self.bullets.empty()
        self.enemies.empty()
