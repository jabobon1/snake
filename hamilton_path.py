from snake import Snake


def hamilton_generator(pos, matrix):
    y, x = pos
    m_len = matrix.shape[0]
    x_add = 0
    while True:
        x_add = int((y - 1) % (m_len - 2) == 0) * int(y > 1 or (x + 1) % 2 == 0) * abs(-1 + abs(x_add))
        x_add -= int(y == 1 and x == m_len - 1) + int(x > 0 == y)
        x += x_add
        y = y + ((-1 + 2 * int(x % 2 == 0)) * abs(-1 + abs(x_add))) * (1 - int(x > 0 == y))
        yield y, x


def choose_dir(pos, need_pos):
    y, x = pos
    if (y, x - 1) == need_pos:
        return 3
    if (y, x + 1) == need_pos:
        return 1
    if (y + 1, x) == need_pos:
        return 2
    if (y - 1, x) == need_pos:
        return 0


if __name__ == '__main__':
    from draw import Grid

    snake = Snake((10, 10))
    hamilton_sol = hamilton_generator(snake.position, snake.matrix)

    grid = Grid(snake.matrix)
    ev_loop = grid.event_loop(fps=35)
    ev_loop.__next__()

    while True:
        action = choose_dir(snake.position, hamilton_sol.__next__())
        # print('action', snake.DIRECTIONS[action])
        obs, rew, done, _ = snake.step(action)
        try:
            ev_loop.send((obs, snake.body.__len__(), not done))
        except StopIteration:
            print('Congratulations!')

        if done:
            break
