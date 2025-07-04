import pygame
import random

POWERUP_SIZE = (30, 30)
POWERUP_DURATION = 5000  # milliseconds

POWERUP_TYPES = {
    "double_shot": {"color": (0, 255, 255)},
    "shield": {"color": (255, 255, 255)},
    "slow_enemies": {"color": (255, 0, 255)},
    "rapid_fire": {"color": (0, 200, 0)},
    "invincibility": {"color": (255, 215, 0)},
    "score_boost": {"color": (255, 165, 0)},
    "clear_screen": {"color": (0, 100, 255)},
    "heal": {"color": (255, 50, 50)}
}

def spawn_powerup(x, y, vy=2):
    kind = random.choice(list(POWERUP_TYPES.keys()))
    rect = pygame.Rect(x, y, *POWERUP_SIZE)
    return {
        "rect": rect,
        "type": kind,
        "color": POWERUP_TYPES[kind]["color"],
        "spawn_time": pygame.time.get_ticks(),
        "vy": vy
    }

def draw_powerups(win, powerups):
    for p in powerups:
        pygame.draw.rect(win, p["color"], p["rect"])

def update_powerups(powerups, player_rect):
    """
    Moves powerups towards the player (downwards or towards player center).
    """
    for p in powerups:
        if p["rect"].centery < player_rect.centery:
            p["rect"].y += p.get("vy", 2)
        if p["rect"].centerx < player_rect.centerx:
            p["rect"].x += 1
        elif p["rect"].centerx > player_rect.centerx:
            p["rect"].x -= 1

def apply_powerup(player_state, ptype):
    if ptype == "double_shot":
        player_state["double_shot"] = True
    elif ptype == "shield":
        player_state["shield"] = True
    elif ptype == "slow_enemies":
        player_state["slow_enemies"] = True
    elif ptype == "rapid_fire":
        player_state["rapid_fire"] = True
    elif ptype == "invincibility":
        player_state["invincibility"] = True
    elif ptype == "score_boost":
        player_state["score_boost"] = True
    elif ptype == "clear_screen":
        player_state["clear_screen"] = True
    elif ptype == "heal":
        if "lives" in player_state:
            player_state["lives"] = min(player_state["lives"] + 1, 5)

    # Ensure timers dict exists for timed powerups
    if ptype != "heal":
        if "timers" not in player_state:
            player_state["timers"] = {}

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
            pygame.draw.rect(win, (50, 50, 50), (10, y_offset + i * (bar_height + spacing), bar_width, bar_height))
            pygame.draw.rect(win, POWERUP_TYPES[ptype]["color"], (10, y_offset + i * (bar_height + spacing), int(bar_width * percent), bar_height))
            i += 1