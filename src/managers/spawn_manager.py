# ==============================================================================
# SPAWN MANAGER - GESTOR DE APARICIÓN DE ENEMIGOS
# ==============================================================================
# Este manager se encarga de crear y gestionar las oleadas de enemigos

import pygame
from src.entities import Enemy
from config import *

class SpawnManager:
    """
    Gestor de aparición de enemigos.
    
    Responsabilidades:
    - Crear oleadas de enemigos en formación
    - Gestionar la dificultad progresiva
    - Controlar el movimiento en formación
    - Detectar victoria (todos los enemigos eliminados)
    """
    
    def __init__(self):
        """
        Constructor del SpawnManager.
        """
        # Nivel actual del juego
        self.current_level = 1
        
        # Configuración de la formación base
        self.base_rows = ENEMY_ROWS
        self.base_cols = ENEMY_COLS
        self.spacing_x = ENEMY_SPACING_X
        self.spacing_y = ENEMY_SPACING_Y
        
        # Margen desde el borde superior
        self.start_y = 50
        
        # Velocidad de movimiento de la formación
        self.formation_speed = ENEMY_SPEED
        
        # Cooldown para evitar descensos múltiples
        # Cuando tocan el borde, no pueden volver a bajar hasta que este timer expire
        self.descent_cooldown = 0  # Tiempo restante de cooldown (segundos)
        self.descent_delay = 0.5   # Medio segundo entre descensos
        
        print("✅ SpawnManager inicializado")
    
    def spawn_wave(self, level, enemy_group, all_sprites):
        """
        Genera una oleada de enemigos según el nivel.
        
        Args:
            level: Nivel actual del juego
            enemy_group: Grupo donde agregar los enemigos
            all_sprites: Grupo de todos los sprites
        
        Returns:
            int: Cantidad de enemigos generados
        """
        print(f"🌊 Generando oleada del nivel {level}...")
        
        # Aumentar dificultad con el nivel
        # Más columnas cada 2 niveles
        rows = self.base_rows
        cols = self.base_cols + (level // 2)
        
        # Calcular ancho total de la formación
        formation_width = (cols - 1) * self.spacing_x
        
        # Centrar la formación horizontalmente
        start_x = (WINDOW_WIDTH - formation_width) // 2
        
        enemies_created = 0
        
        # Crear la formación de enemigos
        for row in range(rows):
            for col in range(cols):
                # Calcular posición del enemigo
                x = start_x + (col * self.spacing_x)
                y = self.start_y + (row * self.spacing_y)
                
                # Determinar tipo de enemigo según la fila
                # Fila 0: tanques (más difíciles)
                # Fila 1-2: básicos
                # Fila 3+: rápidos
                if row == 0:
                    enemy_type = "tank"
                elif row < 3:
                    enemy_type = "basic"
                else:
                    enemy_type = "fast"
                
                # Crear el enemigo
                enemy = Enemy(x, y, enemy_type)
                
                # Agregar a los grupos
                enemy_group.add(enemy)
                all_sprites.add(enemy)
                
                enemies_created += 1
        
        print(f"👾 {enemies_created} enemigos creados en formación {rows}x{cols}")
        return enemies_created
    
    def update_formation(self, enemy_group, delta_time):
        """
        Actualiza el movimiento en formación de los enemigos.
        
        Cuando un enemigo llega al borde de la pantalla:
        - Todos descienden (solo si no hay cooldown activo)
        - Todos invierten dirección
        
        Args:
            enemy_group: Grupo de enemigos a actualizar
            delta_time: Tiempo desde el último frame (segundos)
        
        Returns:
            bool: True si llegaron al fondo (invasión), False si no
        """
        if len(enemy_group) == 0:
            return False
        
        # Actualizar cooldown de descenso
        if self.descent_cooldown > 0:
            self.descent_cooldown -= delta_time
        
        # Verificar si algún enemigo llegó al borde
        hit_left_edge = False
        hit_right_edge = False
        hit_bottom = False
        
        for enemy in enemy_group:
            # Verificar borde izquierdo
            if enemy.rect.left <= 0:
                hit_left_edge = True
            
            # Verificar borde derecho
            if enemy.rect.right >= WINDOW_WIDTH:
                hit_right_edge = True
            
            # Verificar si llegaron al fondo (invasión)
            if enemy.rect.bottom >= WINDOW_HEIGHT - 100:
                hit_bottom = True
        
        # Si alguno llegó al borde horizontal Y no hay cooldown activo
        if (hit_left_edge or hit_right_edge) and self.descent_cooldown <= 0:
            # Todos los enemigos bajan y cambian dirección
            for enemy in enemy_group:
                enemy.move_down()
                enemy.reverse_direction()
            
            # Activar cooldown para evitar descensos múltiples
            self.descent_cooldown = self.descent_delay
            
            print("🔄 Formación descendió y cambió dirección")
        
        # Retornar si hubo invasión
        return hit_bottom
    
    def all_enemies_dead(self, enemy_group):
        """
        Verifica si todos los enemigos han sido eliminados.
        
        Args:
            enemy_group: Grupo de enemigos
        
        Returns:
            bool: True si no quedan enemigos, False si aún hay
        """
        return len(enemy_group) == 0
    
    def next_level(self):
        """
        Avanza al siguiente nivel.
        
        Returns:
            int: Nuevo nivel
        """
        self.current_level += 1
        print(f"🎊 ¡Nivel {self.current_level} desbloqueado!")
        
        # Aumentar velocidad de enemigos progresivamente
        self.formation_speed += 0.2
        
        return self.current_level
    
    def reset(self):
        """
        Reinicia el manager al estado inicial.
        """
        self.current_level = 1
        self.formation_speed = ENEMY_SPEED
        self.descent_cooldown = 0  # Resetear cooldown
        print("🔄 SpawnManager reiniciado")
