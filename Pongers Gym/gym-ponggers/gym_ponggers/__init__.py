#gym-ponggers/gym_ponggers/__init__.py
import gym
from gym.envs.registration import register

register(
    id='ponggers-v0',
    entry_point='gym_ponggers.envs:PonggersEnv',
)

