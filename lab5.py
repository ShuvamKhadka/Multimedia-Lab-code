#creation of basic animation sequence using keyframe animation, demonstrating principles of motion and timing.
import pygame # type: ignore
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keyframe Easing Demonstration")

BACKGROUND = (20, 25, 40)
COLORS = [
    (255, 105, 97),
    (97, 255, 105),
    (105, 97, 255),
    (255, 255, 105)
]

EASING_NAMES = ["Linear", "Ease-In", "Ease-Out", "Ease-In-Out"]
TEXT_COLOR = (200, 220, 255)

balls = []
for i in range(4):
    balls.append({
        'x': 100,
        'y': 150 + i * 100,
        'radius': 20,
        'color': COLORS[i],
        'start_x': 100,
        'end_x': 700,
        'frame': 0,
        'total_frames': 180,
        'easing_type': i
    })

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

def linear(t):
    return t

def ease_in(t):
    return t * t

def ease_out(t):
    return 1 - (1 - t) * (1 - t)

def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    return 1 - 2 * (1 - t) * (1 - t)

def interpolate(ball):
    t = ball['frame'] / ball['total_frames']

    if ball['easing_type'] == 0:
        progress = linear(t)
    elif ball['easing_type'] == 1:
        progress = ease_in(t)
    elif ball['easing_type'] == 2:
        progress = ease_out(t)
    else:
        progress = ease_in_out(t)

    ball['x'] = ball['start_x'] + (ball['end_x'] - ball['start_x']) * progress

    if ball['frame'] < ball['total_frames']:
        ball['frame'] += 1
    else:
        ball['frame'] = 0

def draw():
    screen.fill(BACKGROUND)

    for i in range(4):
        pygame.draw.line(
            screen, (60, 60, 80),
            (100, 150 + i * 100),
            (700, 150 + i * 100), 2
        )

    for i, ball in enumerate(balls):
        pygame.draw.circle(
            screen, ball['color'],
            (int(ball['x']), int(ball['y'])),
            ball['radius']
        )

        label = font.render(EASING_NAMES[i], True, TEXT_COLOR)
        screen.blit(label, (50, ball['y'] - 10))

        progress = ball['frame'] / ball['total_frames'] * 100
        progress_text = font.render(f"{progress:.1f}%", True, TEXT_COLOR)
        screen.blit(progress_text, (ball['x'] - 20, ball['y'] - 40))

    title = font.render(
        "Keyframe Easing Types — Press R to Reset",
        True, TEXT_COLOR
    )
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    explanation = font.render(
        "All balls start and end at the same time, using different easing techniques",
        True, TEXT_COLOR
    )
    screen.blit(explanation, (WIDTH // 2 - explanation.get_width() // 2, 70))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for ball in balls:
                    ball['frame'] = 0
                    ball['x'] = ball['start_x']

    for ball in balls:
        interpolate(ball)

    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
