import pygame
import random
import sys
from auth.auth_utils import get_all_users, login_user, register_user
from game import config
from game import utils
from game import enemy_manager
from game import powerups
from game.boss import Boss
from ui.button import Button
from ui.input_box import InputBox

class PixelInvadersGame:
    def __init__(self, sc):
        pygame.init()
        self.win = sc
        pygame.display.set_caption("Pixel Invaders")
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)
        self.player_img = utils.load_image(config.PLAYER_IMAGE, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self.enemy_basic_img = utils.load_image(config.ENEMY_BASIC_IMAGE, (config.ENEMY_WIDTH, config.ENEMY_HEIGHT))
        self.enemy_medium_img = utils.load_image(config.ENEMY_MEDIUM_IMAGE, (config.ENEMY_WIDTH, config.ENEMY_HEIGHT))
        self.enemy_strong_img = utils.load_image(config.ENEMY_STRONG_IMAGE, (config.ENEMY_WIDTH, config.ENEMY_HEIGHT))
        self.clock = pygame.time.Clock()

    def login_screen(self):
        input_font = pygame.font.SysFont(config.FONT_NAME, 28)
        username_box = InputBox(300, 220, 200, 40, input_font, "Username")
        password_box = InputBox(300, 280, 200, 40, input_font, "Password", is_password=True)

        mode = "login"  # or "signup"
        message = ""

        login_btn = Button("Login", (400, 340), input_font, (255, 255, 255), (0, 255, 0), lambda: None)
        toggle_btn = Button("Switch to Signup", (400, 400), input_font, (200, 200, 200), (255, 255, 0), lambda: None)

        while True:
            self.win.fill((0, 0, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                result = username_box.handle_event(event)
                if result is not None:
                    username_box.set_text(result)

                result = password_box.handle_event(event)
                if result is not None:
                    password_box.set_text(result)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_btn.rect.collidepoint(event.pos):
                        uname = username_box.text
                        pwd = password_box.text
                        if mode == "login":
                            user = login_user(uname, pwd)
                            if user:
                                self.current_user = user
                                self.high_score = user["high_score"]
                                if user["username"].lower() == "admin":
                                    self.admin_panel()
                                return
                            else:
                                message = "Invalid credentials"
                        else:
                            if register_user(uname, pwd):
                                message = "Registered! Please login."
                                mode = "login"
                            else:
                                message = "Username already exists"
                    elif toggle_btn.rect.collidepoint(event.pos):
                        mode = "signup" if mode == "login" else "login"
                        toggle_btn.text = "Switch to Login" if mode == "signup" else "Switch to Signup"
                        toggle_btn.render()

            # Draw UI
            username_box.draw(self.win)
            password_box.draw(self.win)
            login_btn.draw(self.win)
            toggle_btn.draw(self.win)

            title = self.font.render("Login" if mode == "login" else "Signup", True, (255, 255, 255))
            self.win.blit(title, (config.WIDTH//2 - title.get_width()//2, 160))
            if message:
                msg_text = self.font.render(message, True, (255, 100, 100))
                self.win.blit(msg_text, (config.WIDTH//2 - msg_text.get_width()//2, 450))

            pygame.display.update()


    def show_home_screen(self):        
        title_font = pygame.font.SysFont(config.FONT_NAME, 48)
        menu_font = self.font

        last_score = getattr(self, "last_score", 0)
        high_score = utils.load_high_score(config.HIGH_SCORE_FILE)

        start_btn = Button("Start Game", (config.WIDTH // 2, 250), menu_font, (255, 255, 255), (0, 255, 0), self._start_game)
        quit_btn = Button("Quit", (config.WIDTH // 2, 320), menu_font, (255, 100, 100), (255, 0, 0), self._quit_game)

        buttons = [start_btn, quit_btn]

        self.start_requested = False
        while not self.start_requested:
            self.win.blit(utils.load_image(config.BACKGROUND_IMAGE, (config.WIDTH, config.HEIGHT)), (0, 0))

            title = title_font.render("ChronoFleet: 2187", True, (0, 255, 255))
            hs = menu_font.render(f"High Score: {high_score}", True, (200, 200, 100))
            ls = menu_font.render(f"Last Score: {last_score}", True, (180, 180, 180))

            self.win.blit(title, (config.WIDTH // 2 - title.get_width() // 2, 100))
            self.win.blit(hs, (config.WIDTH // 2 - hs.get_width() // 2, 160))
            self.win.blit(ls, (config.WIDTH // 2 - ls.get_width() // 2, 190))

            for btn in buttons:
                btn.draw(self.win)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()
                for btn in buttons:
                    btn.handle_event(event)

    def _start_game(self):
        self.start_requested = True

    def _quit_game(self):
        pygame.quit()
        sys.exit()

    def admin_panel(self):
        panel_font = pygame.font.SysFont(config.FONT_NAME, 24)
        running = True

        while running:
            self.win.fill((20, 20, 30))
            title = self.font.render("Admin Panel - Registered Users", True, (255, 255, 0))
            self.win.blit(title, (config.WIDTH // 2 - title.get_width() // 2, 30))

            users = get_all_users()
            for i, user in enumerate(users):
                u_text = panel_font.render(f"{i+1}. {user[0]} - High Score: {user[2]}", True, (200, 200, 200))
                self.win.blit(u_text, (80, 80 + i * 30))

            note = panel_font.render("Press Q to quit panel", True, (150, 150, 150))
            self.win.blit(note, (config.WIDTH//2 - note.get_width()//2, config.HEIGHT - 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False


    def draw_game(self):
        self.win.blit(utils.load_image(config.BACKGROUND_IMAGE, (config.WIDTH, config.HEIGHT)), (0, 0))
        self.win.blit(self.player_img, self.player)

        for bullet in self.bullets:
            pygame.draw.rect(self.win, config.BULLET_COLOR, bullet)

        for e in self.enemies:
            self.win.blit(e["image"], e["rect"])

        if self.boss:
            self.boss.draw(self.win)

        powerups.draw_powerups(self.win, self.active_powerups)
        powerups.draw_timers(self.win, self.player_state)

        heal_icon = utils.load_image(config.HEAL_ICON, (15, 15))
        for i in range(self.player_state["lives"]):
            # Draw heart icon for each life, use heal icon if "heal" powerup is active
            if heal_icon:
                self.win.blit(heal_icon, (config.WIDTH - 20 * (i+1), 10))
            else:
                pygame.draw.rect(self.win, (255, 50, 50), (config.WIDTH - 20 * (i+1), 10, 15, 15))

        score_text = self.font.render(f"Score: {self.score}  High Score: {self.high_score}", True, config.TEXT_COLOR)
        self.win.blit(score_text, (10, 10))
        # Draw enemy bullets
        for eb in self.enemy_bullets:
            pygame.draw.rect(self.win, (255, 0, 255), eb)  # purple bullets

        pygame.display.update()

    def show_game_over(self):
        text = self.font.render("Game Over! Press R to Restart or Q to Quit", True, config.GAME_OVER_COLOR)
        self.win.blit(text, (config.WIDTH // 2 - text.get_width() // 2, config.HEIGHT // 2))
        pygame.display.update()

    def main_game(self):
        self.player = pygame.Rect(config.WIDTH // 2 - config.PLAYER_WIDTH // 2, config.HEIGHT - 60, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
        self.bullets = []
        self.enemies = enemy_manager.spawn_enemies(self.enemy_basic_img, self.enemy_medium_img, self.enemy_strong_img, (config.ENEMY_WIDTH, config.ENEMY_HEIGHT))
        self.active_powerups = []
        self.player_state = {
            "double_shot": False,
            "shield": False,
            "slow_enemies": False,
            "rapid_fire": False,
            "invincibility": False,
            "score_boost": False,
            "clear_screen": False,
            "heal": False,
            "lives": 3,
            "timers": {}
        }
        level = 1
        self.boss = None
        self.enemy_bullets = []
        self.last_enemy_shot = pygame.time.get_ticks()
        self.enemy_shoot_delay = max(500, 1000 - level * 100)
        boss_level_interval = 3  # Boss appears every 3 levels



        enemy_direction = 1
        enemy_speed = config.ENEMY_INITIAL_SPEED + level * 0.2

        self.score = 0
        self.high_score = utils.load_high_score(config.HIGH_SCORE_FILE)
        last_shot = pygame.time.get_ticks()
        run = True

        while run:
            self.last_score = self.score
            self.clock.tick(config.FPS)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player.x > 0:
                self.player.x -= config.PLAYER_SPEED
            if keys[pygame.K_RIGHT] and self.player.x < config.WIDTH - config.PLAYER_WIDTH:
                self.player.x += config.PLAYER_SPEED
            if keys[pygame.K_SPACE]:
                shoot_delay = config.SHOOT_DELAY
                if self.player_state["rapid_fire"] and "timers" in self.player_state and current_time - self.player_state["timers"].get("rapid_fire", 0) < powerups.POWERUP_DURATION:
                    shoot_delay = 100
                if current_time - last_shot > shoot_delay and len(self.bullets) < config.MAX_BULLETS:
                    bullet = pygame.Rect(self.player.centerx - 2, self.player.y, config.BULLET_WIDTH, config.BULLET_HEIGHT)
                    self.bullets.append(bullet)
                    if self.player_state["double_shot"]:
                        bullet2 = pygame.Rect(self.player.centerx - 15, self.player.y, config.BULLET_WIDTH, config.BULLET_HEIGHT)
                        self.bullets.append(bullet2)
                    last_shot = current_time

            for bullet in self.bullets[:]:
                bullet.y -= config.BULLET_SPEED
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            move_down = False
            for e in self.enemies:
                speed = enemy_speed * 0.5 if self.player_state["slow_enemies"] else enemy_speed
                e["rect"].x += speed * enemy_direction
                if e["rect"].right >= config.WIDTH or e["rect"].left <= 0:
                    move_down = True

            if move_down:
                enemy_direction *= -1
                for e in self.enemies:
                    e["rect"].y += config.ENEMY_DROP_DISTANCE

            if self.boss:
                self.boss.update(config.WIDTH)

            for bullet in self.bullets[:]:
                for e in self.enemies[:]:
                    if bullet.colliderect(e["rect"]):
                        self.score += e["points"] * (2 if self.player_state["score_boost"] else 1)
                        if random.random() < 0.1:
                            self.active_powerups.append(powerups.spawn_powerup(e["rect"].x, e["rect"].y))
                        self.enemies.remove(e)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

            if self.boss:
                for bullet in self.bullets[:]:
                    if self.boss is not None and bullet.colliderect(self.boss.rect):
                        if self.boss.take_damage(5):
                            self.score += 100
                            self.boss = None
                        self.bullets.remove(bullet)

            now = pygame.time.get_ticks()
            if now - self.last_enemy_shot > self.enemy_shoot_delay:
                if self.enemies:
                    shooter = random.choice(self.enemies)
                    bullet = pygame.Rect(shooter["rect"].centerx, shooter["rect"].bottom, 4, 12)
                    self.enemy_bullets.append(bullet)
                if self.boss:
                    boss_bullet = pygame.Rect(self.boss.rect.centerx, self.boss.rect.bottom, 6, 15)
                    self.enemy_bullets.append(boss_bullet)
                self.last_enemy_shot = now

            for eb in self.enemy_bullets[:]:
                eb.y += 5
                if eb.y > config.HEIGHT:
                    self.enemy_bullets.remove(eb)
                elif eb.colliderect(self.player):
                    if not self.player_state.get("invincibility") and not self.player_state.get("shield"):
                        self.player_state["lives"] -= 1
                    self.enemy_bullets.remove(eb)
                    if self.player_state["lives"] <= 0:
                        if self.score > self.high_score:
                            utils.save_high_score(config.HIGH_SCORE_FILE, self.score)
                        self.show_game_over()
                        return

            powerups.update_powerups(self.active_powerups, self.player)
            powerups.check_powerup_collisions(self.player, self.player_state, self.active_powerups)

            self.active_powerups = [p for p in self.active_powerups if current_time - p["spawn_time"] < powerups.POWERUP_DURATION]

            expired = [ptype for ptype, start in self.player_state["timers"].items() if current_time - start > powerups.POWERUP_DURATION]
            for ptype in expired:
                if ptype in self.player_state:
                    self.player_state[ptype] = False
                del self.player_state["timers"][ptype]

            if self.player_state["clear_screen"]:
                self.enemies.clear()
                self.boss = None
                self.player_state["clear_screen"] = False
                
            # Check level completion
            if not self.enemies and not self.boss:
                level += 1
                self.display_level_transition(level)

                # Boss appears every few levels
                if level % boss_level_interval == 0:
                    self.boss = Boss(100, 50, self.enemy_strong_img)
                    self.enemies = []  # Ensure no other enemies
                else:
                    self.enemies = enemy_manager.spawn_enemies(
                        self.enemy_basic_img, self.enemy_medium_img, self.enemy_strong_img, (config.ENEMY_WIDTH, config.ENEMY_HEIGHT))
                    enemy_speed += config.ENEMY_RESPAWN_SPEED_INCREMENT

            if any(e["rect"].bottom >= config.HEIGHT - 60 for e in self.enemies) or (self.boss and self.boss.rect.bottom >= config.HEIGHT - 60):
                if not self.player_state["invincibility"] and not self.player_state["shield"]:
                    self.player_state["lives"] -= 1
                    if self.player_state["lives"] <= 0:
                        if self.score > self.high_score:
                            utils.save_high_score(config.HIGH_SCORE_FILE, self.score)
                        self.show_game_over()
                        return

                    else:
                        self.enemies = enemy_manager.spawn_enemies(
                            self.enemy_basic_img, self.enemy_medium_img, self.enemy_strong_img, 
                            (config.ENEMY_WIDTH, config.ENEMY_HEIGHT)
                        )
                        self.boss = None

            self.draw_game()

    def display_level_transition(self, level):
        text = self.font.render(f"Level {level}!", True, (255, 255, 255))
        self.win.fill((0, 0, 0))
        self.win.blit(text, (config.WIDTH // 2 - text.get_width() // 2, config.HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def run(self):
        self.login_screen()
        while True:
            self.show_home_screen()
            self.main_game()
            self.last_score = self.score
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
