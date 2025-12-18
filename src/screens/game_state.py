from abc import ABC, abstractmethod
from time import time

class GameState(ABC):

    """
    Clase base abstracta para todos los estados del juego.
    
    Un estado representa una "pantalla" o "modo" del juego:
    - Loading Screen
    - Menu Screen
    - Playing Screen
    - Pause Screen
    - Game Over Screen
    
    Cada estado tiene su propia lógica de:
    - Eventos (teclas presionadas)
    - Actualización (física, IA, etc.)
    - Renderizado (qué se dibuja)
    """

    def __init__(self, game):
        """
        Constructor base de todos los estados.
        
        Args:
            game: Referencia a la instancia principal del juego
                  Esto nos permite acceder a screen, clock, etc.
        """
        self.game = game
        self.screen = game.screen
        

    @abstractmethod
    def handle_events(self, events: list) -> None:
        """
        Maneja los eventos específicos de este estado.
        
        Args:
            events: Lista de eventos de pygame (teclas, mouse, etc.)
        
        ABSTRACTO: Cada estado DEBE implementar este método.
        Por ejemplo:
        - En MENU: detectar selección de opciones
        - En PLAYING: detectar disparos, movimiento
        - En PAUSE: detectar resumir/salir
        """
        pass

    @abstractmethod
    def update(self, delta_time: time) -> None:
        """
        Actualiza la lógica del estado.
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame (en segundos)
                       Útil para movimientos independientes del framerate
        
        ABSTRACTO: Cada estado DEBE implementar este método.
        - En PLAYING: mover jugador, enemigos, balas
        - En LOADING: actualizar barra de progreso
        - En MENU: animaciones de fondo
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Dibuja los elementos visuales del estado.
        
        ABSTRACTO: Cada estado DEBE implementar este método.
        Por ejemplo:
        - En MENU: título, opciones, cursor
        - En PLAYING: jugador, enemigos, balas, HUD
        - En GAME_OVER: puntuación final, mensaje
        """
        pass

    @abstractmethod
    def enter(self):
        """
        Se ejecuta UNA VEZ cuando entramos a este estado.
        
        Útil para:
        - Inicializar variables
        - Cargar recursos específicos
        - Reproducir música de fondo
        - Resetear valores
        
        """
        print("Entering state:", self.__class__.__name__)

    @abstractmethod
    def exit(self):
        """
        Se ejecuta UNA VEZ cuando salimos de este estado.
        
        Útil para:
        - Limpiar recursos
        - Detener música
        - Guardar datos
        
        """
        print("Exiting state:", self.__class__.__name__)