import random

import pygame
import setup
from random import choice

pygame.init()
screen = pygame.display.set_mode((setup.WIDTH, setup.HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

player = None
apple = None


def draw_square(color, left, top):
    width = height = setup.SQUARE - 2 * setup.MARGIN
    pygame.draw.rect(screen, color, (left + setup.MARGIN, top + setup.MARGIN, width, height))


def update_frame():
    screen.fill("black")
    update_part_map()
    update_player()
    update_apple()


def update_part_map():
    for part in setup.part_map:
        color = setup.BORDER_COLOR if part.part_type is setup.PT.BORDER else setup.ISLAND_COLOR
        draw_square(color, part.x*setup.SQUARE, part.y*setup.SQUARE)


def update_player():

    if not isinstance(player, setup.Snake):
        raise TypeError()

    temp = player.head
    while temp is not None:
        left = temp.x * setup.SQUARE
        top = temp.y * setup.SQUARE
        color = player.color
        draw_square(color, left, top)
        temp = temp.Next


def generate_new_apple():
    global apple
    # x, y = setup.generate_random_square(setup.APPLE_SPAWN_PADDING)
    x, y = random.choice(setup.available_squares)
    apple = setup.Part(x, y, setup.PT.APPLE)
    apple.color = choice(list(setup.APPLE_COLORS))


def update_apple():
    if not isinstance(apple, setup.Part):
        return None

    left = apple.x * setup.SQUARE
    top = apple.y * setup.SQUARE
    draw_square(apple.color, left, top)


def handle_keys():
    if not isinstance(player, setup.Snake):
        raise TypeError()

    keys = pygame.key.get_pressed()
    x, y = 0, 0
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y = -1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y = 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x = 1

    prev_direction = player.Direction
    if x == 0 and y == 1:
        player.Direction = setup.Direction.DOWN
    if x == 0 and y == -1:
        player.Direction = setup.Direction.UP
    if x == 1 and y == 0:
        player.Direction = setup.Direction.RIGHT
    if x == -1 and y == 0:
        player.Direction = setup.Direction.LEFT
    if x == 1 and y == 1:
        player.Direction = setup.Direction.RIGHT_DOWN
    if x == -1 and y == -1:
        player.Direction = setup.Direction.LEFT_UP
    if x == 1 and y == -1:
        player.Direction = setup.Direction.UP_RIGHT
    if x == -1 and y == 1:
        player.Direction = setup.Direction.DOWN_LEFT

    if (player.Direction.value + 4) % 8 == prev_direction.value:
        player.Direction = prev_direction


def handle_logic() -> bool:
    """
    Checks if the player hits the borders or itself
    and check if ate an apple.

    returns True if the snake didn't hit the border.
    """
    if not isinstance(player, setup.Snake):
        raise TypeError()

    # Self collision check
    temp = player.head
    temp = temp.Next
    while temp is not None:
        if player.head.check_overlap(temp):
            return False
        temp = temp.Next

    if (player.head.x, player.head.y) in setup.part_map_xy:
        return False

    player_ate = False
    if apple is not None and player.head.check_overlap(apple):
        player_ate = True
        generate_new_apple()
        player.score += 1

    player.move_in_direction(player_ate)

    return True


def restart_game():
    global player
    setup.generate_part_map()
    player = setup.Snake()
    generate_new_apple()


def main():
    restart_game()
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_logic() is False:
            restart_game()

        update_frame()
        handle_keys()
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(setup.snake_speed) / 1000

    pygame.quit()


def game_over():
    setup.snake_speed = 0


if __name__ == "__main__":
    main()
