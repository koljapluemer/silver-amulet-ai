import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from gym.envs.registration import register
from gym.utils.env_checker import check_env

from amulet import GridWorldEnv

# not working
register(id='CustomEnv-v0', entry_point='envs/amulet.py:GridWorldEnv')

# env = make_vec_env("CustomEnv-v0", n_envs=4)
env = gym.make("CustomEnv-v0")
wrapped_env = FlattenObservation(env)


model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo_amulet")