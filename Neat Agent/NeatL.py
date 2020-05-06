import gym
import gym_ponggers
import neat
import numpy as np
import os
import pygame

def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    nets = []
    ge = []
    env = []

    for genome in genomes:
        net = neat.nn.feed_forward.FeedForwardNetwork.create(genome[1], config)
        genome[1].fitness = 0
        nets.append(net)
        temp_env = gym.make('ponggers-v0')
        env.append(temp_env)
        ge.append(genome[1])

    print(nets)
    print(ge)

    bestRewardIndex = -1001
    x = 0
    while x < len(ge):
        cur_env = gym.make('ponggers-v0')
        agentA = nets[x]
        agentB = nets[x + 1]
        temp_best = -1000
        actionA = 1
        actionB = 4
        for i in range(1000):
            if i == 1:
                obs, reward, done, info = cur_env.step([1,4])
            else:
                obs, reward, done, info = cur_env.step([actionA, actionB])
            #to watch :)
            #cur_env.render()
            obs = cur_env.observation()
            print(len(obs))
            listA = agentA.activate(obs)
            listB = agentB.activate(obs)
            actionA = getAction(listA, "A")
            actionB = getAction(listB, "B")
        if bestRewardIndex > temp_best:
            bestRewardIndex = temp_best
        x = x + 2

def getAction(list, agent):
    action = 0
    best = list[0]
    if agent == "A":
        placeholder = 0
    else:
        placeholder = 3
    for x in list:
        if best > x:
            best = x
            action = placeholder
        placeholder = placeholder + 1
    return action

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    generation_num = 50
    winner = p.run(eval_genomes, generation_num)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
