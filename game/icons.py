import pygame


def draw_rock(surface, center, size):
    x, y = center

    points = [
        (x - size // 2, y + size // 3),
        (x - size // 2 + 8, y - size // 4),
        (x - size // 4, y - size // 2),
        (x + size // 4, y - size // 2 + 5),
        (x + size // 2, y - size // 5),
        (x + size // 2 - 5, y + size // 3),
        (x + size // 4, y + size // 2),
        (x - size // 4, y + size // 2),
    ]

    pygame.draw.polygon(surface, (125, 130, 140), points)
    pygame.draw.polygon(surface, (220, 220, 225), points, width=3)


def draw_paper(surface, center, size):
    x, y = center

    rect = pygame.Rect(
        x - size // 2,
        y - size // 2,
        size,
        int(size * 1.25),
    )

    pygame.draw.rect(surface, (235, 235, 240), rect, border_radius=6)
    pygame.draw.rect(surface, (220, 220, 225), rect, width=3, border_radius=6)

    line_color = (100, 105, 115)

    for offset in [-18, 0, 18]:
        pygame.draw.line(
            surface,
            line_color,
            (x - size // 3, y + offset),
            (x + size // 3, y + offset),
            3,
        )


def draw_scissors(surface, center, size):
    x, y = center

    blade_color = (210, 215, 225)

    pygame.draw.line(
        surface,
        blade_color,
        (x - 8, y - 5),
        (x + size // 2, y - size // 2),
        10,
    )

    pygame.draw.line(
        surface,
        blade_color,
        (x - 8, y + 5),
        (x + size // 2, y + size // 2),
        10,
    )

    pygame.draw.circle(
        surface,
        (70, 75, 85),
        (x - 15, y - 20),
        13,
    )

    pygame.draw.circle(
        surface,
        (70, 75, 85),
        (x - 15, y + 20),
        13,
    )

    pygame.draw.circle(
        surface,
        (220, 220, 225),
        (x - 15, y - 20),
        6,
    )

    pygame.draw.circle(
        surface,
        (220, 220, 225),
        (x - 15, y + 20),
        6,
    )


def draw_question_mark(surface, center, font):
    text = font.render("?", True, (245, 245, 245))
    surface.blit(
        text,
        (
            center[0] - text.get_width() // 2,
            center[1] - text.get_height() // 2,
        ),
    )


def draw_choice_icon(surface, choice, center, size, font):
    if choice == "ROCK":
        draw_rock(surface, center, size)
    elif choice == "PAPER":
        draw_paper(surface, center, size)
    elif choice == "SCISSORS":
        draw_scissors(surface, center, size)
    else:
        draw_question_mark(surface, center, font)