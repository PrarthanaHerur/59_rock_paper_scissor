
import random
import pygame
from game.button import ChoiceButton
from game.icons import draw_choice_icon


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton("ROCK", pygame.Rect(start_x, btn_y, btn_w, btn_h), (160, 50, 50), (200, 70, 70)),
            ChoiceButton("PAPER", pygame.Rect(start_x + btn_w + gap, btn_y, btn_w, btn_h), (40, 100, 170), (60, 130, 210)),
            ChoiceButton("SCISSORS", pygame.Rect(start_x + 2 * (btn_w + gap), btn_y, btn_w, btn_h), (180, 140, 30), (220, 180, 50)),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0

        self.winning_score = 3
        self.match_over = False
        self.match_winner = None

        self.recent_player_choices = []
        self.history_limit = 5

        self.reveal_in_progress = False
        self.reveal_start_time = 0
        self.reveal_duration = 2400
        self.round_outcome = None

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_countdown = pygame.font.SysFont(None, 58)
        self.font_icon = pygame.font.SysFont(None, 72)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"
            
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }
        return rules.get((player, cpu), "TIE")

    def get_adaptive_cpu_choice(self):
        if len(self.recent_player_choices) < 3:
            return random.choice(self.choices)

        counts = {
            "ROCK": self.recent_player_choices.count("ROCK"),
            "PAPER": self.recent_player_choices.count("PAPER"),
            "SCISSORS": self.recent_player_choices.count("SCISSORS"),
        }

        most_common_choice = max(counts, key=counts.get)

        counter_moves = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }

        counter_move = counter_moves[most_common_choice]

        if random.random() < 0.70:
            return counter_move

        return random.choice(self.choices)

    def play_round(self, choice):
        if self.match_over or self.showing_result or self.reveal_in_progress:
            return

        self.player_choice = choice
        self.recent_player_choices.append(choice)

        if len(self.recent_player_choices) > self.history_limit:
            self.recent_player_choices.pop(0)

        self.cpu_choice = self.get_adaptive_cpu_choice()

        self.round_outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice,
        )

        self.reveal_in_progress = True
        self.reveal_start_time = pygame.time.get_ticks()
        self.result_text = "Get Ready!"
        self.result_color = (220, 225, 235)

    def resolve_round(self):
        outcome = self.round_outcome

        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = f"You Win! {self.player_choice} beats {self.cpu_choice}."
            self.result_color = (80, 230, 120)

            if self.player_score >= self.winning_score:
                self.match_over = True
                self.match_winner = "PLAYER"

        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            self.result_color = (240, 80, 80)

            if self.cpu_score >= self.winning_score:
                self.match_over = True
                self.match_winner = "CPU"

        else:
            self.result_text = f"It's a Draw! Both picked {self.player_choice}."
            self.result_color = (240, 210, 80)

        self.reveal_in_progress = False
        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    def reset_match(self):
        self.player_score = 0
        self.cpu_score = 0
        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)
        self.match_over = False
        self.match_winner = None
        self.recent_player_choices = []
        self.reveal_in_progress = False
        self.round_outcome = None
        self.showing_result = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if self.match_over:
                self.reset_match()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()

        if self.reveal_in_progress:
            if now - self.reveal_start_time >= self.reveal_duration:
                self.resolve_round()
            return

        if self.showing_result and (now - self.round_resolved_time >= self.display_duration):
            if self.match_over:
                if self.match_winner == "PLAYER":
                    self.result_text = "PLAYER WINS THE MATCH! Press R to restart."
                    self.result_color = (80, 230, 120)
                else:
                    self.result_text = "CPU WINS THE MATCH! Press R to restart."
                    self.result_color = (240, 80, 80)
            else:
                self.player_choice = None
                self.cpu_choice = None
                self.result_text = "Make your move!"
                self.result_color = (190, 195, 205)
                self.showing_result = False

    def render_reveal(self, screen):
        elapsed = pygame.time.get_ticks() - self.reveal_start_time

        if elapsed < 600:
            countdown_text = "3"
        elif elapsed < 1200:
            countdown_text = "2"
        elif elapsed < 1800:
            countdown_text = "1"
        else:
            countdown_text = "GO!"

        countdown_surf = self.font_countdown.render(
            countdown_text,
            True,
            (245, 245, 245),
        )

        screen.blit(
            countdown_surf,
            (
                self.width // 2 - countdown_surf.get_width() // 2,
                205,
            ),
        )

        left_center = (self.width // 2 - 135, 160)
        right_center = (self.width // 2 + 135, 160)

        pygame.draw.circle(
            screen,
            (45, 52, 66),
            left_center,
            70,
        )

        pygame.draw.circle(
            screen,
            (45, 52, 66),
            right_center,
            70,
        )

        if elapsed >= 1800:
            draw_choice_icon(
                screen,
                self.player_choice,
                left_center,
                65,
                self.font_icon,
            )

            draw_choice_icon(
                screen,
                self.cpu_choice,
                right_center,
                65,
                self.font_icon,
            )
        else:
            draw_choice_icon(
                screen,
                None,
                left_center,
                65,
                self.font_icon,
            )

            draw_choice_icon(
                screen,
                None,
                right_center,
                65,
                self.font_icon,
            )

        player_label = self.font_hud.render(
            "PLAYER",
            True,
            (100, 180, 255),
        )

        cpu_label = self.font_hud.render(
            "CPU",
            True,
            (255, 120, 120),
        )

        screen.blit(
            player_label,
            (
                left_center[0] - player_label.get_width() // 2,
                85,
            ),
        )

        screen.blit(
            cpu_label,
            (
                right_center[0] - cpu_label.get_width() // 2,
                85,
            ),
        )

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245),
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14,
            ),
        )

        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255),
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120),
        )

        screen.blit(p_surf, (35, 52))
        screen.blit(
            c_surf,
            (self.width - c_surf.get_width() - 35, 52),
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2,
        )

        if self.reveal_in_progress:
            self.render_reveal(screen)
        else:
            p_str = self.player_choice if self.player_choice else "--"
            c_str = self.cpu_choice if self.cpu_choice else "--"

            arena_p = self.font_arena.render(
                f"Your Pick:  {p_str}",
                True,
                (225, 225, 230),
            )

            arena_c = self.font_arena.render(
                f"CPU Pick:  {c_str}",
                True,
                (225, 225, 230),
            )

            screen.blit(
                arena_p,
                (
                    self.width // 2 - arena_p.get_width() // 2,
                    115,
                ),
            )

            screen.blit(
                arena_c,
                (
                    self.width // 2 - arena_c.get_width() // 2,
                    155,
                ),
            )

            res_surf = self.font_arena.render(
                self.result_text,
                True,
                self.result_color,
            )

            screen.blit(
                res_surf,
                (
                    self.width // 2 - res_surf.get_width() // 2,
                    205,
                ),
            )

        for btn in self.buttons:
            btn.render(screen)