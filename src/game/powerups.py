import pygame
import random
from game import config
from game import utils

# Constants
POWERUP_SIZE = config.POWERUP_SIZE
POWERUP_DURATION = 5000  # milliseconds

# Define powerups (initially without icons)
POWERUP_TYPES = {
    "double_shot": {"color": (0, 255, 255)},
    "shield": {"color": (255, 255, 255)},
    "slow_enemies": {"color": (255, 0, 255)},
    "rapid_fire": {"color": (0, 200, 0)},
    "invincibility": {"color": (255, 215, 0)},
    "score_boost": {"color": (255, 165, 0)},
    "clear_screen": {"color": (0, 100, 255)},
    "heal": {"color": (255, 50, 50)},
}

# 🔧 Call this after pygame.display.set_mode()
def init_powerup_icons():
    POWERUP_TYPES["double_shot"]["icon"] = utils.load_image(config.DOUBLE_SHOT_ICON, POWERUP_SIZE)
    POWERUP_TYPES["shield"]["icon"] = utils.load_image(config.SHIELD_ICON, POWERUP_SIZE)
    POWERUP_TYPES["slow_enemies"]["icon"] = utils.load_image(config.SLOW_ENEMIES_ICON, POWERUP_SIZE)
    POWERUP_TYPES["rapid_fire"]["icon"] = utils.load_image(config.RAPID_FIRE_ICON, POWERUP_SIZE)
    POWERUP_TYPES["invincibility"]["icon"] = utils.load_image(config.INVINCIBILITY_ICON, POWERUP_SIZE)
    POWERUP_TYPES["score_boost"]["icon"] = utils.load_image(config.SCORE_BOOST_ICON, POWERUP_SIZE)
    POWERUP_TYPES["clear_screen"]["icon"] = utils.load_image(config.CLEAR_SCREEN_ICON, POWERUP_SIZE)
    POWERUP_TYPES["heal"]["icon"] = utils.load_image(config.HEAL_ICON, POWERUP_SIZE)

# Spawn a powerup
def spawn_powerup(x, y, vy=2):
    kind = random.choice(list(POWERUP_TYPES.keys()))
    rect = pygame.Rect(x, y, *POWERUP_SIZE)
    icon = POWERUP_TYPES.get(kind, {}).get("icon")
    return {
        "rect": rect,
        "type": kind,
        "color": POWERUP_TYPES[kind]["color"],
        "spawn_time": pygame.time.get_ticks(),
        "vy": vy,
        "icon": icon
    }

# Draw powerups
def draw_powerups(win, powerups):
    for p in powerups:
        pygame.draw.rect(win, p["color"], p["rect"], border_radius=6)
        if "icon" in p and p["icon"]:
            icon_rect = p["icon"].get_rect(center=p["rect"].center)
            win.blit(p["icon"], icon_rect)

# Update powerups (falling toward player)
def update_powerups(powerups, player_rect):
    for p in powerups:
        if p["rect"].centery < player_rect.centery:
            p["rect"].y += p.get("vy", 2)
        if p["rect"].centerx < player_rect.centerx:
            p["rect"].x += 1
        elif p["rect"].centerx > player_rect.centerx:
            p["rect"].x -= 1

# Apply powerup effect
def apply_powerup(player_state, ptype):
    if ptype == "heal":
        if "lives" in player_state:
            player_state["lives"] = min(player_state["lives"] + 1, 5)
    else:
        player_state[ptype] = True
        if "timers" not in player_state:
            player_state["timers"] = {}

# Check collisions and activate powerup
def check_powerup_collisions(player_rect, player_state, powerups):
    collected = []
    for p in powerups:
        if player_rect.colliderect(p["rect"]):
            apply_powerup(player_state, p["type"])
            collected.append(p)
            if p["type"] != "heal":
                player_state["timers"][p["type"]] = pygame.time.get_ticks()
    for p in collected:
        powerups.remove(p)

# Timer bar drawing for active powerups
def draw_timers(win, player_state, y_offset=40):
    current_time = pygame.time.get_ticks()
    bar_width = 100
    bar_height = 6
    spacing = 10
    i = 0
    for ptype, start_time in player_state.get("timers", {}).items():
        elapsed = current_time - start_time
        if elapsed < POWERUP_DURATION:
            percent = 1 - (elapsed / POWERUP_DURATION)
            x = 10
            y = y_offset + i * (bar_height + spacing)
            pygame.draw.rect(win, (50, 50, 50), (x, y, bar_width, bar_height))
            pygame.draw.rect(win, POWERUP_TYPES[ptype]["color"], (x, y, int(bar_width * percent), bar_height))
            icon = POWERUP_TYPES.get(ptype, {}).get("icon")
            if icon:
                icon_rect = icon.get_rect(topleft=(x + bar_width + 6, y - 3))
                win.blit(icon, icon_rect)
            i += 1

# Auto-expire finished powerups
def cleanup_expired_powerups(player_state):
    current_time = pygame.time.get_ticks()
    expired = []
    for ptype, start_time in player_state.get("timers", {}).items():
        if current_time - start_time > POWERUP_DURATION:
            expired.append(ptype)
    for ptype in expired:
        player_state[ptype] = False
        del player_state["timers"][ptype]
