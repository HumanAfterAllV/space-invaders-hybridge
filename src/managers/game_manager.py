import pygame


class GameManager():
    """
    Manager principal del juego (Patrón Singleton).
    
    SINGLETON: Solo puede existir UNA instancia de esta clase en todo el programa.
    
    Responsabilidades:
    - Gestionar el estado actual del juego
    - Cambiar entre estados (loading → menu → playing → etc.)
    - Delegar eventos, update y draw al estado actual
    """

    _instance = None

    def __new__(cls, game = None):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.current_state = None
            cls._instance.game = game
        return cls._instance
    
    def __init__(self, game = None):
        if self._instance:
            return
        
        self.game = game
        self.current_state = None
        self.previous_state = None

        self._initialized = True
        print("GameManager inicializado.")

    def change_state(self, new_state) -> None:
        """
        Cambia al nuevo estado del juego.
        
        Flujo:
        1. Salir del estado actual (cleanup)
        2. Guardar estado actual como "anterior"
        3. Establecer nuevo estado
        4. Entrar al nuevo estado (inicialización)
        
        Args:
            new_state: Instancia del nuevo estado (LoadingScreen, MenuScreen, etc.)
        """

        if self.current_state is not None:
            print(f"Saliendo del estado: {type(self.current_state).__name__}")
            self.current_state.exit()
            self.previous_state = self.current_state

        self.current_state = new_state

        if self.current_state is not None:
            print(f"Entrando al estado: {type(self.current_state).__name__}")
            self.current_state.enter()



    def handle_events(self, events: list) -> None:
        """
        Delega el manejo de eventos al estado actual.
        
        Args:
            events: Lista de eventos de pygame
        """
        if self.current_state is not None:
            self.current_state.handle_events(events)
    
    def update(self, delta_time):
        """
        Delega la actualización al estado actual.
        
        Args:
            delta_time: Tiempo desde el último frame (en segundos)
        """
        if self.current_state is not None:
            self.current_state.update(delta_time)
    
    def draw(self):
        """
        Delega el renderizado al estado actual.
        """
        if self.current_state is not None:
            self.current_state.draw()
    
    def go_back(self):
        """
        Vuelve al estado anterior.
        
        Útil para:
        - Volver del menú de pausa al juego
        - Volver de opciones al menú principal
        """
        if self.previous_state is not None:
            print("⬅️ Volviendo al estado anterior...")
            self.change_state(self.previous_state)