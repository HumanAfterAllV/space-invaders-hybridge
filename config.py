# ==============================================================================
# CONFIGURACIÓN GLOBAL DEL JUEGO SPACE INVADERS
# ==============================================================================
# Este archivo centraliza todas las constantes para facilitar ajustes
# y mantener el código limpio sin "números mágicos"

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE VENTANA
# ------------------------------------------------------------------------------
WINDOW_WIDTH = 800      # Ancho de la ventana en píxeles
WINDOW_HEIGHT = 600     # Alto de la ventana en píxeles
WINDOW_TITLE = "Space Invaders - Hybridge Edition"
FPS = 60                # Frames por segundo (suavidad del juego)

# ------------------------------------------------------------------------------
# COLORES (formato RGB)
# ------------------------------------------------------------------------------
# Usamos tuplas RGB (Red, Green, Blue) con valores 0-255
BLACK = (0, 0, 0)           # Fondo del espacio
WHITE = (255, 255, 255)     # Texto y elementos UI
RED = (255, 0, 0)           # Indicadores de daño
GREEN = (0, 255, 0)         # Indicadores de vida/salud
BLUE = (0, 100, 255)        # Color principal del jugador
YELLOW = (255, 255, 0)      # Power-ups y efectos especiales
CYAN = (0, 255, 255)        # Enemigos tipo 1
MAGENTA = (255, 0, 255)     # Enemigos tipo 2
GRAY = (128, 128, 128)      # UI y menús

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DEL JUGADOR
# ------------------------------------------------------------------------------
PLAYER_WIDTH = 50           # Ancho de la nave del jugador
PLAYER_HEIGHT = 40          # Alto de la nave del jugador
PLAYER_SPEED = 5            # Velocidad de movimiento horizontal (px/frame)
PLAYER_LIVES = 3            # Vidas iniciales
PLAYER_SHOOT_COOLDOWN = 250 # Milisegundos entre disparos (evita spam)

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE BALAS
# ------------------------------------------------------------------------------
BULLET_WIDTH = 5            # Ancho de la bala
BULLET_HEIGHT = 15          # Alto de la bala
BULLET_SPEED = 7            # Velocidad de la bala (px/frame)
BULLET_COLOR = YELLOW       # Color de las balas del jugador
ENEMY_BULLET_COLOR = RED    # Color de las balas enemigas

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE ENEMIGOS (valores base)
# ------------------------------------------------------------------------------
ENEMY_WIDTH = 40            # Ancho base del enemigo
ENEMY_HEIGHT = 30           # Alto base del enemigo
ENEMY_SPEED = 1             # Velocidad horizontal base
ENEMY_ROWS = 4              # Número de filas de enemigos
ENEMY_COLS = 8              # Número de columnas de enemigos
ENEMY_SPACING_X = 60        # Espacio horizontal entre enemigos
ENEMY_SPACING_Y = 50        # Espacio vertical entre filas
ENEMY_DESCENT_SPEED = 20    # Cuánto bajan cuando llegan al borde

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE PUNTUACIÓN
# ------------------------------------------------------------------------------
SCORE_ENEMY_BASIC = 10      # Puntos por enemigo básico
SCORE_ENEMY_FAST = 20       # Puntos por enemigo rápido
SCORE_ENEMY_TANK = 30       # Puntos por enemigo tanque
SCORE_BOSS = 100            # Puntos por jefe (futuro)

# ------------------------------------------------------------------------------
# ESTADOS DEL JUEGO
# ------------------------------------------------------------------------------
# Enumeración de estados posibles (usaremos esto para el patrón State)
STATE_LOADING = "loading"   # Pantalla de carga inicial
STATE_MENU = "menu"         # Menú principal
STATE_PLAYING = "playing"   # Jugando
STATE_PAUSED = "paused"     # Pausa
STATE_GAME_OVER = "gameover" # Fin del juego
STATE_VICTORY = "victory"   # Victoria

# ------------------------------------------------------------------------------
# RUTAS DE ASSETS (recursos multimedia)
# ------------------------------------------------------------------------------
# Definimos las rutas relativas a los archivos multimedia
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"