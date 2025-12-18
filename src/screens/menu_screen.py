import pygame
from config import *
from src.screens.game_state import GameState

class MenuScreen(GameState):
    """
    Pantalla del menú principal del juego.
    
    Características:
    - Navegación con teclado (flechas o WASD)
    - Feedback visual de la opción seleccionada
    - Transiciones a otros estados según la opción elegida
    """

    def __init__(self, game):
        super().__init__(game)

        # Opciones del menú
        self.options = ["Play", "Quit"]
        
        # Índice de la opción actualmente seleccionada
        self.selected_option = 0
        
        # Fuente para el título del juego
        self.font_title = None 
        self.font_subtitle = None       
        self.font_options = None
        self.font_controls = None
        
        # Colores para opciones normales y seleccionadas
        self.color_selected = YELLOW
        self.color_normal = WHITE
        
        # Espaciado entre opciones (en píxeles)
        self.options_spacing = 60

        # Posición Y
        self.options_start_y = 300

    def enter(self):
        """
        Se ejecuta al entrar al menú principal.
        
        Inicializa fuentes y resetea la selección.
        """
        print("🎬 Entrando al Menu Screen")

        # Cargar fuentes
        self.font_title = pygame.font.SysFont('arial', 64, bold=True)
        self.font_subtitle = pygame.font.SysFont('arial', 24, italic=True)
        self.font_options = pygame.font.SysFont('arial', 36, bold=True)
        self.font_controls = pygame.font.SysFont('arial', 18)

        # Resetear selección
        self.selected_option = 0

        # TODO: Reproducir música del menú

    def handle_events(self, events):
        """
        Maneja la navegación del menú y la selección de opciones.
        
        Controles:
        - FLECHA_ARRIBA / W: Navegar hacia arriba
        - FLECHA_ABAJO / S: Navegar hacia abajo
        - ENTER / SPACE: Seleccionar opción
        
        Args:
            events: Lista de eventos de pygame
        """

        for event in events:
            if event.type == pygame.KEYDOWN:

                # Navegación hacia arriba
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.navigate_up()

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.navigate_down()

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.select_option()
    
    def navigate_up(self):
        
        self.selected_option -= 1

        if self.selected_option < 0:
            # Si pasamos de la primera opción, ir a la ultima
            self.selected_option = len(self.options) - 1

        print(f"Opción seleccionada: {self.options[self.selected_option]}")

        # TODO: Reproducir sonido de navegación

    def navigate_down(self):

        self.selected_option += 1

        if self.selected_option >= len(self.options):
            # Si pasamos de la primera opción, ir a la ultima
            self.selected_option = 0

        print(f"Opción seleccionada: {self.options[self.selected_option]}")

        # TODO: Reproducir sonido de navegación

    def select_option(self):
        """
        Ejecuta la acción de la opción seleccionada.
        
        Opciones:
        - 0 (PLAY): Iniciar el juego (cambiar a GameScreen)
        - 1 (OPTIONS): Abrir configuración (cambiar a OptionsScreen)
        - 2 (EXIT): Salir del juego
        """
        option_name = self.options[self.selected_option]
        print(f"✅ Opción seleccionada: {option_name}")
        
        # TODO: Reproducir sonido de selección
        # self.sound_select.play()
        
        if self.selected_option == 0:  # PLAY
            print("🎮 Iniciando juego...")
            # Cambiar a GameScreen
            from src.screens.game_screen import GameScreen
            self.game.game_manager.change_state(GameScreen(self.game))
        
        elif self.selected_option == 1:  # EXIT
            print("👋 Saliendo del juego...")
            # Cerrar el juego (establecer running = False)
            self.game.running = False
    
    def update(self, delta_time):
        """
        Actualiza la lógica del menú.
        
        Por ahora no hay animaciones complejas, pero aquí podríamos:
        - Animar el título
        - Hacer parpadear la opción seleccionada
        - Mover estrellas del fondo
        
        Args:
            delta_time: Tiempo desde el último frame (en segundos)
        """
        # TODO: Agregar animaciones si se desea
        # Por ahora el menú es estático
        pass
    
    def draw(self):
        """
        Dibuja el menú principal en pantalla.
        
        Elementos:
        - Fondo negro
        - Título del juego
        - Subtítulo
        - Opciones del menú (resaltando la seleccionada)
        - Instrucciones de control
        """
        # 1. Limpiar pantalla con fondo negro
        self.screen.fill(BLACK)
        
        # TODO: Dibujar fondo con estrellas (opcional)
        # self.draw_stars_background()
        
        # 2. Dibujar título principal
        title_text = self.font_title.render("SPACE INVADERS", True, CYAN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # 3. Dibujar subtítulo
        subtitle_text = self.font_subtitle.render("Hybridge Edition", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 4. Dibujar línea decorativa debajo del título
        line_y = 190
        pygame.draw.line(
            self.screen, 
            CYAN, 
            (WINDOW_WIDTH // 2 - 200, line_y),  # Punto inicial
            (WINDOW_WIDTH // 2 + 200, line_y),  # Punto final
            2  # Grosor de la línea
        )
        
        # 5. Dibujar opciones del menú
        for i, option in enumerate(self.options):
            # Calcular posición Y de esta opción
            # Comienza en options_start_y y se incrementa por option_spacings
            option_y = self.options_start_y + (i * self.options_spacing)
            
            # Determinar si esta opción está seleccionada
            is_selected = (i == self.selected_option)
            
            # Elegir color según si está seleccionada
            color = self.color_selected if is_selected else self.color_normal
            
            # Renderizar el texto de la opción
            option_text = self.font_options.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, option_y))
            
            # Si está seleccionada, dibujar indicador ">"
            if is_selected:
                # Dibujar indicador a la izquierda
                indicator_left = self.font_options.render(">", True, color)
                indicator_left_rect = indicator_left.get_rect(
                    right=option_rect.left - 20,  # 20px a la izquierda del texto
                    centery=option_y
                )
                self.screen.blit(indicator_left, indicator_left_rect)
                
                # Dibujar indicador a la derecha
                indicator_right = self.font_options.render("<", True, color)
                indicator_right_rect = indicator_right.get_rect(
                    left=option_rect.right + 20,  # 20px a la derecha del texto
                    centery=option_y
                )
                self.screen.blit(indicator_right, indicator_right_rect)
            
            # Dibujar el texto de la opción
            self.screen.blit(option_text, option_rect)
        
        # 6. Dibujar instrucciones de control en la parte inferior
        controls_text = "↑/↓ Navigate    ENTER Select    ESC Exit"
        controls_surface = self.font_controls.render(controls_text, True, GRAY)
        controls_rect = controls_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )
        self.screen.blit(controls_surface, controls_rect)
    
    def exit(self):
        """
        Se ejecuta al salir del menú principal.
        
        Limpieza de recursos (música, etc.)
        """
        print("🚪 Saliendo del Menu Screen")
        
        # TODO: Detener música de menú
        # pygame.mixer.music.stop()


    