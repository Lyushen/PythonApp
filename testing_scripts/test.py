import pygame as pg
import random

def SnakeGame():
    tile_size = 25
    window_width = 800
    window_height = 600

    def get_random_position():
        x_position = random.randrange(tile_size, window_width - tile_size, tile_size)
        y_position = random.randrange(tile_size, window_height - tile_size, tile_size)
        return [x_position, y_position]

    snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
    snake.center = get_random_position()
    length = 1
    snake_dir = (0, 0)
    time, time_step = 0, 110
    segments = [snake.copy()]
    food = snake.copy()
    food.center = get_random_position()

    pg.init()
    screen = pg.display.set_mode((window_width, window_height))
    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                # Handle key presses based on current direction for smoother controls:
                if event.key == pg.K_w and snake_dir != (0, tile_size):
                    snake_dir = (0, -tile_size)
                elif event.key == pg.K_s and snake_dir != (0, -tile_size):
                    snake_dir = (0, tile_size)
                elif event.key == pg.K_a and snake_dir != (tile_size, 0):
                    snake_dir = (-tile_size, 0)
                elif event.key == pg.K_d and snake_dir != (-tile_size, 0):
                    snake_dir = (tile_size, 0)

        screen.fill('black')

        # Wrap snake around the borders seamlessly:
        new_x, new_y = snake.center[0] + snake_dir[0], snake.center[1] + snake_dir[1]
        if new_x < 0:
            new_x = window_width - tile_size // 2  # Wrap to opposite side
        elif new_x >= window_width:
            new_x = tile_size // 2  # Wrap to opposite side
        if new_y < 0:
            new_y = window_height - tile_size // 2  # Wrap to opposite side
        elif new_y >= window_height:
            new_y = tile_size // 2  # Wrap to opposite side
        snake.center = (new_x, new_y)

        # Check for collision with food
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1

        pg.draw.rect(screen, 'red', food)  # Draw food
        [pg.draw.rect(screen, 'green', segment) for segment in segments]  # Draw snake

        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

        pg.display.flip()
        clock.tick(60)  # Maintain consistent frame rate