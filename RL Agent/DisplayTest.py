import gym
import pygame
import gym_ponggers

pygame.init()
display = pygame.display.set_mode((350, 350))


env=gym.make('ponggers-v0')

for i in range(0, 100):
    state, reward, done, _ = env.step([1,3])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
