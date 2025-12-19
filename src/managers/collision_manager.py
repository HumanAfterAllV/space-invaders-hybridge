# ==============================================================================
# COLLISION MANAGER - GESTOR DE COLISIONES
# ==============================================================================
# Este manager detecta y maneja todas las colisiones del juego

import pygame
from config import *

class CollisionManager:
    """
    Gestor de colisiones del juego.
    
    Responsabilidades:
    - Detectar colisiones entre balas y enemigos
    - Detectar colisiones entre balas y jugador
    - Detectar colisiones entre enemigos y jugador
    - Calcular puntuación por eliminaciones
    """
    
    def __init__(self):
        """
        Constructor del CollisionManager.
        """
        print("✅ CollisionManager inicializado")
    
    def check_bullet_enemy_collisions(self, player_bullets, enemies):
        """
        Detecta colisiones entre balas del jugador y enemigos.
        
        Args:
            player_bullets: Grupo de balas del jugador
            enemies: Grupo de enemigos
        
        Returns:
            int: Puntos ganados por las eliminaciones
        """
        # groupcollide(grupo1, grupo2, kill_grupo1, kill_grupo2)
        # Retorna un diccionario: {sprite_grupo1: [sprites_grupo2_colisionados]}
        # True = eliminar sprite al colisionar
        # False = no eliminar (útil para enemigos con más vida)
        
        collisions = pygame.sprite.groupcollide(
            player_bullets,  # Balas del jugador
            enemies,         # Enemigos
            True,            # Eliminar bala al impactar
            False            # NO eliminar enemigo automáticamente (maneja vida)
        )
        
        total_points = 0
        enemies_to_kill = []  # Lista de enemigos que murieron
        
        # Procesar cada colisión
        for bullet, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                # El enemigo recibe daño
                points = enemy.take_damage(damage=1)
                total_points += points
                
                # Si murió, agregarlo a la lista de eliminación
                if points > 0:
                    enemies_to_kill.append(enemy)
                
                # TODO: Crear efecto de explosión si murió
                # if points > 0:
                #     self.create_explosion(enemy.rect.center)
        
        # ELIMINAR INMEDIATAMENTE los enemigos muertos
        for enemy in enemies_to_kill:
            enemy.kill()  # Forzar eliminación de todos los grupos
        
        if total_points > 0:
            print(f"💰 +{total_points} puntos! ({len(enemies_to_kill)} enemigos destruidos)")
        
        return total_points
    
    def check_bullet_player_collisions(self, enemy_bullets, player):
        """
        Detecta colisiones entre balas de enemigos y el jugador.
        
        Args:
            enemy_bullets: Grupo de balas enemigas
            player: Sprite del jugador
        
        Returns:
            bool: True si el jugador fue golpeado, False si no
        """
        # spritecollide(sprite, grupo, kill_grupo)
        # Retorna lista de sprites del grupo que colisionaron
        hit_bullets = pygame.sprite.spritecollide(
            player,        # Jugador
            enemy_bullets, # Balas enemigas
            True           # Eliminar balas al impactar
        )
        
        # Si hubo colisión
        if hit_bullets:
            # El jugador recibe daño
            player.take_damage()
            return True
        
        return False
    
    def check_enemy_player_collisions(self, enemies, player):
        """
        Detecta colisiones directas entre enemigos y el jugador.
        
        Esto ocurre cuando un enemigo toca físicamente al jugador.
        
        Args:
            enemies: Grupo de enemigos
            player: Sprite del jugador
        
        Returns:
            bool: True si hubo colisión, False si no
        """
        hit_enemies = pygame.sprite.spritecollide(
            player,   # Jugador
            enemies,  # Enemigos
            False     # NO eliminar enemigo (game over de todas formas)
        )
        
        # Si algún enemigo tocó al jugador
        if hit_enemies:
            print("💥 ¡Enemigo impactó al jugador!")
            # El jugador recibe daño masivo (game over)
            player.take_damage()
            return True
        
        return False
    
    def check_enemy_invasion(self, enemies):
        """
        Verifica si algún enemigo llegó al fondo de la pantalla.
        
        Esto representa una "invasión" y es game over.
        
        Args:
            enemies: Grupo de enemigos
        
        Returns:
            bool: True si hubo invasión, False si no
        """
        # Línea de invasión (cerca del fondo)
        invasion_line = WINDOW_HEIGHT - 100
        
        for enemy in enemies:
            if enemy.rect.bottom >= invasion_line:
                print("🚨 ¡INVASIÓN! Los enemigos llegaron al fondo!")
                return True
        
        return False
    
    def check_all_collisions(self, game_screen):
        """
        Método conveniente que verifica todas las colisiones.
        
        Args:
            game_screen: Instancia del GameScreen con todos los grupos
        
        Returns:
            dict: Diccionario con resultados de las colisiones
        """
        results = {
            'points_gained': 0,
            'player_hit': False,
            'enemy_collision': False,
            'invasion': False
        }
        
        # 1. Balas del jugador vs enemigos
        results['points_gained'] = self.check_bullet_enemy_collisions(
            game_screen.player_bullets,
            game_screen.enemies
        )
        
        # 2. Balas de enemigos vs jugador
        results['player_hit'] = self.check_bullet_player_collisions(
            game_screen.enemy_bullets,
            game_screen.player
        )
        
        # 3. Enemigos vs jugador (colisión directa)
        results['enemy_collision'] = self.check_enemy_player_collisions(
            game_screen.enemies,
            game_screen.player
        )
        
        # 4. Invasión (enemigos llegaron al fondo)
        results['invasion'] = self.check_enemy_invasion(
            game_screen.enemies
        )
        
        return results
