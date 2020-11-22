import numpy as np
import random


class Snake:
    DIRECTIONS = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}
    ACTIONS = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])

    def __init__(self, shape):
        self.matrix = np.zeros(shape)
        self.body = np.array([(0, 3), (0, 4)])

        self.draw_body()

        self.direction = 2
        self.add_mushroom()

    def reset(self):
        self.matrix = np.zeros(self.matrix.shape)
        self.body = np.array([(0, 3), (0, 4)])
        self.draw_body()

        self.direction = 2
        self.add_mushroom()
        return self.matrix, 0, False, None

    @property
    def position(self):
        return tuple(self.body[0])

    @property
    def mushroom(self):
        mushroom = np.where(self.matrix == 2)
        return mushroom[0][0], mushroom[1][0]

    def add_mushroom(self):
        free_space = [pos for pos in zip(*np.where(self.matrix == 0))]
        if not free_space:
            return False

        self.matrix[random.choice(free_space)] = 2.

        return True

    def draw_body(self):
        for pos in self.body:
            self.matrix[tuple(pos)] = 1.

    @property
    def alive(self):
        check_1 = not np.where(self.body < 0)[0].size and not np.where(self.body >= self.matrix.shape)[0].size
        # val = self.body[0]
        # check_2 = not np.where(self.body[1:] == val)[0].size
        check_2 = all(tuple(part) != tuple(self.body[0]) for part in self.body[1:])

        return check_1 and check_2

    def action_is_allowed(self, action):
        res = self.ACTIONS[self.direction] + self.ACTIONS[action] != [0, 0]
        return res.any()

    def step(self, action):
        reward = 0
        body = self.body.copy()

        if not self.action_is_allowed(action):
            action = self.direction

        self.direction = action
        self.body[0] += self.ACTIONS[action]

        # moving rest body for right positions
        for idx, node in enumerate(body[:-1]):
            self.body[idx + 1] = node

        # add previous tail to the current body
        if self.mushroom == tuple(self.body[0]):
            self.body = np.append(self.body, np.expand_dims(body[-1], axis=0), axis=0)
            new_m = self.add_mushroom()
            reward += 1
            # if there is no place for new mushroom game is finished
            if not new_m:
                reward += 9
                return self.matrix, reward, True, None

        alive = self.alive

        if alive:
            # clean previous body
            self.matrix[np.where(self.matrix == 1)] = 0.
            self.draw_body()
            reward += 0.1
        else:
            reward -= 5

        return self.matrix, reward, not alive, None


if __name__ == '__main__':
    snake = Snake((10, 10))
    print(snake.position, '\n')
    while True:
        action = random.randint(0, 3)
        obs, rew, done, _ = snake.step(action)
        print(obs, '\n')
        if done:
            break
