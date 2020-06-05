import gym
import gym_ponggers
import neat
import numpy as np
import os
import pygame
import sys
import time

scoresList = []
hitsList = []

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
        ge.append(genome[1])

    x = 0
    game_render = False
    left_list = []
    right_list = []
    while x < len(ge):
        cur_env = gym.make('ponggers-v0', render=game_render)
        agentA = nets[x]
        agentB = nets[x + 1]
        actionA = -1
        actionB = -1
        for i in range(1000):
            obs, reward, done, info = cur_env.step([actionA, actionB])
            obs = cur_env.observation()
            listA = agentA.activate(obs)
            listB = agentB.activate(obs)
            actionA = getAction(listA, "A")
            actionB = getAction(listB, "B")
        ge[x].fitness = fitnessFunc(cur_env, "A")
        ge[x + 1].fitness = fitnessFunc(cur_env, "B")
        scoresList.append(cur_env.getScores()[0])
        scoresList.append(cur_env.getScores()[1])
        print("Score List")
        print(scoresList)
        hitsList.append(cur_env.getPaddleAHits())
        hitsList.append(cur_env.getPaddleBHits())
        print("Hit List")
        print(hitsList)
        print("Game " + str(x/2) + " done")
        left_list.append(x)
        right_list.append(x + 1)
        x = x + 2

def transformSpecies(list):

    return list

def returnCombinedLists(listL, listR):
    combine = []
    i = 1
    if len(listL) != len(listR):
        return "The genome lists are not of equal length and cannot be computed"
    while i <= len(listL):
        combine.append((i, listL[i]))
        combine.append((i + 1), listR[i])
    return combine

def returnBestGenomes(list, breeding_threshold):
    best_list = []
    i = 0
    while i < breeding_threshold:
        best_fit = list[0].fitness
        counter = 0
        saved = counter
        for x in list:
            if x.fitness > best_fit:
                best_fit = x.fitness
                saved = counter
            counter = counter + 1
        best_list.append(list.pop(saved))
    return best_list


def fitnessFunc(environment, str):
    scoreA = environment.getScores()[0]
    A_hits = environment.getPaddleAHits()
    scoreB = environment.getScores()[1]
    B_hits = environment.getPaddleBHits()
    hit_incentive = 2
    score_penalty = 3
    if str == "A":
        return scoreA - score_penalty*scoreB + A_hits*hit_incentive
    else:
        return scoreB - score_penalty*scoreA + B_hits*hit_incentive


def getAction(list, agent):
    index = list.index(max(list))
    if agent == "A":
         return index
    else:
        return index + 3


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
    result = p.run(eval_genomes, generation_num)
    winner = result[0]
    final_population = result[1]
    agentType = returnAgentType(winner, final_population)
    print("Agent Type")
    print(agentType)
    winner_net = neat.nn.feed_forward.FeedForwardNetwork.create(winner, config) 
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    new_env = gym.make("ponggers-v0", render=True)
    actionA = -1
    actionB = 0
    while True:
        if agentType == "A":
            obs, reward, done, info = new_env.step([actionA, 4])
        else:
            obs, reward, done, info = new_env.step([1, actionB])
        new_env.render()
        listA = winner_net.activate(obs)
        listB = winner_net.activate(obs)
        actionA = getAction(listA, "A")
        actionB = getAction(listB, "B")


def returnAgentType(genome, population):
    i = 0
    for x in population.values():
        if x == genome:
            if i % 2 == 0:
                return "A"
            else:
                return "B"
        i = i + 1
    return None


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
