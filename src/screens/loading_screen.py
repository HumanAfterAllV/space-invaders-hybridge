import pygame
from src.screens import GameState
from config import *


class LoadingScreen(GameState):
    """
    Pantalla de carga inicial del juego.
    
    Simula la precarga de recursos y muestra una barra de progreso.
    Cuando termina (100%), cambia automáticamente al menú principal.
    """
    def __init__(self, game):

        # Llamar al constructor de la base(GameState)
        super().__init__(game)

        # Progreso de carga (0.0 a 0%, 1.0 = 100%)
        self.progress = 0.0
        
        # Velocidad de carga simulada
        self.load_speed = 0.3

        self.total_resources = 10  # Número total de recursos a cargar
        self.loaded_resources = 0  # Recursos cargados hasta ahora

        self.font_large = None
        self.font_small = None

    def enter(self):
        """
        Inicialización del estado de carga.
        
        Aquí se configuran las fuentes y otros elementos necesarios.
        """

        print("Entrando en LoadingScreen...")

        # Cargar fuentes
        self.font_large = pygame.font.SysFont('arial', 48, bold=True)
        self.font_small = pygame.font.SysFont('arial', 24)

        # Resetear progreso
        self.progress = 0.0
        self.loaded_resources = 0

    def handle_events(self, events):
        """
        Maneja eventos de esta pantalla.
        
        Por ahora no hacemos nada (carga automática).
        Opcional: podríamos permitir saltar con SPACE.
        
        Args:
            events: Lista de eventos de pygame
        """

        # TODO: Opcional - presionar SPACE para saltar la carga

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.progress = 1.0  # Saltar a 100%
                    print("Carga saltada por el usuario.")

    def update(self, delta_time):
        """
        Actualiza la lógica de la pantalla de carga.
        
        Incrementa el progreso gradualmente hasta llegar al 100%.
        Cuando termina, cambia al siguiente estado.
        
        Args:
            delta_time: Tiempo desde el último frame (en segundos)
        """

        if self.progress < 1.0:
            # Incrementar el progreso basado en el tiempo
            self.progress += self.load_speed * delta_time

            # Asegurar que no pasemos del 100%
            if self.progress > 1.0:
                self.progress = 1.0

            # Simular carga de recursos
            expected_loaded = int(self.progress * self.total_resources)

            # Si cargamos un nuevo recurso, mostramos mensaje
            if expected_loaded > self.loaded_resources:
                self.loaded_resources = expected_loaded
                print(f"Cargando recurso {self.loaded_resources}/{self.total_resources}...")

        elif self.progress >= 1.0:
            # Cambio al menú principal cuando la carga termina
            from src.screens.menu_screen import MenuScreen
            self.game.game_manager.change_state(MenuScreen(self.game))
            print("Carga completa. Cambiando al MenuScreen...")

    def draw(self):
        """
        Dibuja la pantalla de carga.
        
        Elementos visuales:
        - Fondo negro
        - Título del juego
        - Texto "LOADING..."
        - Barra de progreso
        - Porcentaje numérico
        """
        # 1. Limpiar pantalla de fondo negro
        self.screen.fill(BLACK)

        # 2. Dibujar titulo del juego
        # render(texto, antialias, color)
        title_text = self.font_large.render("SPACE INVADERS", True, WHITE)
        subtitle_text = self.font_small.render("Hybridge Edition", True, GRAY)

        # Centrar títulos
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 200))

        # blit() dibuja una superficie en otra
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)

        # 3. Dibujar texto "LOADING..."
        loading_text = self.font_small.render("LOADING...", True, WHITE)
        loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(loading_text, loading_rect)

        # 4. Dibujar barra de progreso
        # Dimensiones de la barra
        bar_width = 400
        bar_height = 30
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 350

        # Barra exterior (borde)
        border_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, WHITE, border_rect, 2)  # 2 píxeles de grosor

        # Barra interior (progreso)
        # Se calcula el ancho basado en el progreso actual
        fill_width = int(bar_width * self.progress)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
        pygame.draw.rect(self.screen, GREEN, fill_rect) # Relleno verde

        # 5. Dibujar porcentaje numérico
        percent = int(self.progress * 100)
        percent_text = self.font_small.render(f"{percent}%", True, WHITE)
        percent_rect = percent_text.get_rect(center=(WINDOW_WIDTH // 2,  400))
        self.screen.blit(percent_text, percent_rect)

        if self.progress < 1.0:
            hint_text = self.font_small.render("Press SPACE to skip", True, GRAY)
            hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, 450))
            self.screen.blit(hint_text, hint_rect)

    def exit(self):
        print("Saliendo de LoadingScreen...")
        return super().exit()

