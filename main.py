import pygame
import sys

from config import *
from src.managers import GameManager
from src.screens import LoadingScreen

class Game:
    """
    Clase principal que maneja la inicialización y el game loop.
    
    Aquí integraremos:
    - Sistema de estados (loading, menu, playing)
    - Managers (colisiones, spawn, etc.)
    - Grupos de sprites
    """
    def __init__(self):
        
        # Inicialización de Pygame
        pygame.init()

        # Crear la ventana del juego con las dimensiones definidas en config.py
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # Establecer el título de la ventana
        pygame.display.set_caption(WINDOW_TITLE)

        ## Crear el reloj para controlar los FPS
        # El reloj nos ayudará a mantener una velocidad constante de frames por segundo
        self.clock = pygame.time.Clock()

        # Variable que controla si el juego está corriendo
        self.running = True

        # Inicializar el GameManager (singleton)
        self.game_manager = GameManager(self)

        self.game_manager.change_state(LoadingScreen(self)) 

        # Tiempo transcurrido entre frames
        self.delta_time = 0

        self.clock = pygame.time.Clock()
    
    def handle_events(self):
        """
        Maneja todos los eventos de pygame (teclado, mouse, cerrar ventana).
        
        Los eventos son acciones del usuario:
        - Cerrar la ventana
        - Presionar teclas
        - Mover el mouse
        - etc.
        """

        events = pygame.event.get()
        
        # Iterar sobre todos los eventos en la cola de eventos
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.game_manager.handle_events(events)
    # TODO: Agregar más métodos para manejar lógica del juego.
    def update(self):
        """
        Actualiza el estado del juego.
        
        Aquí se actualizarán:
        - Posiciones de sprites
        - Lógica de colisiones
        - Estados del juego
        """

        self.game_manager.update(self.delta_time)
        pass

    def draw(self):
        """
        Dibuja todos los elementos en la pantalla.
        
        Aquí se dibujarán:
        - Fondo
        - Sprites del jugador y enemigos
        - UI (puntuación, vidas, etc.)

        IMPORTANTE: El orden de dibujo importa!
        - Lo que se dibuja primero queda DEBAJO
        - Lo que se dibuja al final queda ENCIMA

        Orden típico:
        1. Fondo
        2. Enemigos
        3. Balas
        4. Jugador
        5. UI (puntuación, vidas)
        """
        
        # Llenar la pantalla con el color de fondo (negro)
        self.game_manager.draw()
        pygame.display.flip()
        #TODO: Dibujar los sprites

    def run(self):
        """
        Game Loop principal
        
        Método con el ciclo infinito que mantiene el juego corriendo
        """

        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update()
            self.draw()
        
        self.cleanup()

    def cleanup(self):
        """
        Limpieza final antes de cerrar el juego.
        
        Es buena práctica liberar recursos:
        - Cerrar pygame
        - Guardar puntuaciones
        - Liberar memoria
        """

        print("Limpiando recursos...")
        pygame.quit()
        sys.exit()


        

if __name__ == "__main__":
    print("=" * 60)
    print("🌌 SPACE INVADERS - HYBRIDGE EDITION 🌌")
    print("=" * 60)

    game = Game()
    game.run()
