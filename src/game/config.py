# === Screen ===
WIDTH = 800
HEIGHT = 600

# === Player ===
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 40
PLAYER_SPEED = 5
SHOOT_DELAY = 300  # milliseconds

# === Enemy ===
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_INITIAL_SPEED = 1.0
ENEMY_DROP_DISTANCE = 20
ENEMY_RESPAWN_SPEED_INCREMENT = 0.2

# === Bullet ===
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 255, 0)
MAX_BULLETS = 3
BULLET_SPEED = 10

# === Colors ===
BG_COLOR = (10, 10, 30)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 0, 0)

# === Assets ===
ASSETS_PATH = "assets/"
PLAYER_IMAGE = ASSETS_PATH + "player.png"
ENEMY_BASIC_IMAGE = ASSETS_PATH + "enemy_basic.png"
ENEMY_MEDIUM_IMAGE = ASSETS_PATH + "enemy_medium.png"
ENEMY_STRONG_IMAGE = ASSETS_PATH + "enemy_strong.png"

# === Background ===
BACKGROUND_IMAGE = ASSETS_PATH + "bg.jpeg"
HOME_BACKGROUND_IMAGE = ASSETS_PATH + "home_bg.jpeg"

# === Power-ups ===
POWERUP_SIZE = (30, 30)
POWERUP_DURATION = 5000  # milliseconds

# === Power-up icon ===
ICON_PATH = ASSETS_PATH + "icons/"
# Powerup icon paths (all placed inside /assets/icons/)
DOUBLE_SHOT_ICON = "assets/icons/double_shot.png"
SHIELD_ICON = "assets/icons/shield.png"
SLOW_ENEMIES_ICON = "assets/icons/slow_enemies.png"
RAPID_FIRE_ICON = "assets/icons/rapid_fire.png"
INVINCIBILITY_ICON = "assets/icons/invincibility.png"
SCORE_BOOST_ICON = "assets/icons/score_boost.png"
CLEAR_SCREEN_ICON = "assets/icons/clear_screen.png"
HEAL_ICON = "assets/icons/heal.png"


# === Files ===
HIGH_SCORE_FILE = "data/highscore.txt"

# === Fonts ===
FONT_NAME = "arial"
FONT_SIZE = 28

# === Game Settings ===
FPS = 60
