# Imports

import random
import sys
from random import randint

import gym
import math
import pygame
from gym import spaces
import gym_ponggers

# Colour Definitions

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# BALL

class Ball(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.height = height
        self.width = width
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velX = randint(3, 6)
        self.velY = randint(3, 6)
        self.mag = math.pow(self.velX, 2) + math.pow(self.velY, 2)
        self.velocity = [self.velX, self.velY]

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self, speed):
        if self.velocity[0] > 0:
            self.velocity[0] = -(self.velocity[0] + speed)
        else:
            self.velocity[0] = -(self.velocity[0] - speed)
        if self.velocity[1] > 0:
            self.velocity[1] = self.velocity[1] + speed
        else:
            self.velocity[1] = self.velocity[1] - speed
        # randint(-8,8)

    def bounceSpecial(self, speed):
        if self.velocity[0] > 0:
            self.velocity[0] = -(self.velocity[0] + speed)
        else:
            self.velocity[0] = -(self.velocity[0] - speed)
        if self.velocity[1] > 0:
            self.velocity[1] = self.velocity[1] + speed * 2
        else:
            self.velocity[1] = self.velocity[1] - speed * 2

    def reset(self, speed):
        x_reset = randint(340, 360)
        y_reset = randint(240, 260)
        self.rect.x = x_reset
        self.rect.y = y_reset

        # Set a random angle on reset
        self.randAngle(speed)

    def randAngle(self, speed):
        x_comp = random.uniform(math.cos(math.pi / 6), math.cos(math.pi / 3))
        y_comp = random.uniform(math.sin(math.pi / 3), math.sin(math.pi / 6))

        x_rand = randint(1, 2)
        y_rand = randint(1, 2)
        # x
        if x_rand == 1:
            self.velocity[0] = x_comp * speed + self.velX
        else:
            self.velocity[0] = -(x_comp * speed) - self.velX
        # y
        if y_rand == 1:
            self.velocity[1] = y_comp * speed + self.velY
        else:
            self.velocity[1] = -y_comp * speed + self.velY

    def resetA(self):
        y_reset = randint(240, 260)
        x_reset = randint(340, 360)
        self.rect.y = y_reset
        self.rect.x = x_reset
        # self.velocity[0] = -(self.velocity[0])
        rand_vel_y = randint(1, 2)
        if rand_vel_y == 2:
            self.velocity[1] = -(self.velocity[1])

    def resetB(self):
        y_reset = randint(240, 260)
        x_reset = randint(340, 360)
        self.rect.y = y_reset
        self.rect.x = x_reset
        # self.velocity[0] = -(self.velocity[0])
        rand_vel_y = randint(1, 2)
        if rand_vel_y == 2:
            self.velocity[1] = -(self.velocity[1])

    def returnHeight(self):
        return self.height

    def returnWidth(self):
        return self.width


# PADDLE


class Paddle(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y > 400:
            self.rect.y = 400


# FINAL


class Ponggers:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self):

        # Set up and initialize window for the game
        pygame.init()
        size = (700, 500)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Ponggers")

        # Initialize paddles
        self.paddleA = Paddle(self.WHITE, 10, 100)
        self.paddleB = Paddle(self.WHITE, 10, 100)

        # Initialize ball
        ball_w = 10
        ball_h = 10
        self.ball = Ball(self.WHITE, ball_w, ball_h)
        self.initObjs()

        # Sprite list for drawing objects on the screen
        self.all_sprites_list = pygame.sprite.Group()
        self.addSprites()

        # Clock used to control screen update time / frame rate
        self.clock = pygame.time.Clock()

        # Initializing scores
        self.scoreA = 0
        self.scoreB = 0
        self.paddleHits = 0

        # This determines how fast the ball's velocity will increase on each point scored
        self.score_rate = 0.1
        # self.score_mult = self.paddleHits * self.score_rate
        self.boolean_score = False

    def run(self, action):
        self.boolean_score = False
        self.action(action)
        self.all_sprites_list.update()
        self.paddleCollision()
        self.scoreCheck()
        self.clock.tick(60)
        # If x is clicked, close the game
        if pygame.key.get_pressed()[pygame.K_x]:
            self.close()

    def reset(self):
        self.scoreA = 0
        self.scoreB = 0
        self.initObjs()

    def checkSpecialHit(self):
        yA = self.paddleA.rect.y
        yB = self.paddleB.rect.y
        ballY = self.ball.rect.y
        if (yA < ballY < yA + 25) or (yA + 75 < ballY < yA + 100):
            print("Hurah")
            return True
        if (yB < ballY < yB + 25) or (yB + 75 < ballY < yB + 100):
            print("Hurah")
            return True

    def paddleCollision(self):
        # Once the ball is at a certain velocity, the ball will phase / clip right through the paddle and not register as a hit
        # thus, we must ensure that the agent does not receive a penalty for doing the right thing but the program not being correct
        x_proj = self.ball.velocity[0] + self.ball.rect.x
        y_proj = self.ball.velocity[1] + self.ball.rect.y
        line = pygame.draw.line(self.screen, self.RED, (self.ball.rect.x, self.ball.rect.y), (x_proj, y_proj), 3)
        # Double collision check
        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB) or pygame.Rect.colliderect(line, self.paddleA) or pygame.Rect.colliderect(line, self.paddleB):
            self.paddleHits = self.paddleHits + 1
            score_mult = self.paddleHits * self.score_rate
            if self.checkSpecialHit():
                self.ball.bounceSpecial(score_mult)
            else:
                self.ball.bounce(score_mult)

    def scoreCheck(self):
        score_mult = self.paddleHits * self.score_rate
        if self.ball.rect.x >= 690:
            self.scoreA += 1
            self.paddleHits = 0
            self.ball.reset(score_mult)
            self.boolean_score = True
        if self.ball.rect.x < 0:
            self.scoreB += 1
            self.paddleHits = 0
            self.ball.reset(score_mult)
            self.boolean_score = True
        if self.ball.rect.y > 490:
            self.ball.velocity[1] = -(self.ball.velocity[1])
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -(self.ball.velocity[1])

    def action(self, action):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                # carryOn = False # Flag that we are done so we exit this loop
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    # carryOn=False
                    pass
        keys = pygame.key.get_pressed()
        paddle_vel = 5
        if keys[pygame.K_w] or action == 1:
            self.paddleA.moveUp(paddle_vel)
        if keys[pygame.K_s] or action == 2:
            self.paddleA.moveDown(paddle_vel)
        if keys[pygame.K_UP]:
            self.paddleB.moveUp(paddle_vel)
        if keys[pygame.K_DOWN]:
            self.paddleB.moveDown(paddle_vel)

    def display(self):
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.screen.fill(self.BLACK)

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        self.all_sprites_list.draw(self.screen)

        # Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, self.WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(str(self.scoreB), 1, self.WHITE)
        self.screen.blit(text, (420, 10))

    @staticmethod
    def close():
        sys.exit()

    def initObjs(self):
        self.initBall()
        self.initPaddles()

    def initBall(self):
        self.ball.rect.x = 345
        self.ball.rect.y = 195

    def initPaddles(self):
        self.paddleA.rect.x = 0
        self.paddleA.rect.y = 200

        self.paddleB.rect.x = 690
        self.paddleB.rect.y = 200

    def addSprites(self):
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

    @staticmethod
    def get_surface():
        return pygame.display.get_surface()


# ENV

class PonggersEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    # up, down, stay
    pong_actions = 3
    agent_count = 1
    total_pong_actions = agent_count * pong_actions
    width, height = 750, 500
    size = (width, height)

    def __init__(self):
        """
        ACTION SPACE -
            agentA:
            0 = stay
            1 = up
            2 = down
        """
        self.agentA = 0
        self.ponggers = Ponggers()
        self.action_space = spaces.Discrete(self.total_pong_actions)
        self.observation_space = spaces.Box(low=0, high=255, shape=[self.height, self.width, 3])

    def step(self, actionA):
        self.action_space = spaces.Discrete(self.total_pong_actions)
        # print(actionA)
        self.ponggers.run(actionA)

        """
        return:
            observation
            reward
            done
            info
        """

        reward = self.reward()
        observation = self.observation()
        return observation, reward, False, ''

    def reset(self):
        self.action_space = spaces.Discrete(self.total_pong_actions)
        self.ponggers.reset()

    def render(self, mode='human'):
        self.action_space = spaces.Discrete(self.total_pong_actions)
        self.ponggers.display()

    def close(self):
        self.action_space = spaces.Discrete(self.total_pong_actions)
        self.ponggers.close()

    def reward(self):
        if self.ponggers.boolean_score:
            reward = 1000
        else:
            reward = -1
        return reward

    def observation(self):
        currentSurface = self.ponggers.get_surface()
        pixelArray = pygame.surfarray.array3d(currentSurface)
        # print(pygame.PixelArray(currentSurface).shape)

        evalSurf = pygame.surfarray.make_surface(pixelArray)

        return evalSurf

        # return pixelArray[:, :, 0]



