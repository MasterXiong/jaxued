import matplotlib.pyplot as plt
import numpy as np
import pickle
import os


def filter(x, y, mode=1):
    return y[x == mode]

def smooth(x, window_size=50):
    return np.convolve(x, np.ones(window_size), 'valid') / window_size

folders = [
    'plr', 
    'accel', 
    'dr_fake', 
    'accel_robust', 
    'plr_diversity', 
]

plt.figure()
for folder in folders:
    replay_maze_avg_distance = []
    seeds = os.listdir(f'logs/{folder}')
    for seed in seeds:
        with open(f'logs/{folder}/{seed}/mean_maze_distance.pkl', 'rb') as f:
            mean_maze_distance, iter_mode = pickle.load(f)
        mean_maze_distance = np.concatenate(mean_maze_distance)
        iter_mode = np.concatenate(iter_mode)
        # if folder == 'dr_fake':
        #     replay_maze_avg_distance.append(smooth(filter(iter_mode, mean_maze_distance, mode=0)))
        # else:
        #     replay_maze_avg_distance.append(smooth(filter(iter_mode, mean_maze_distance)))
        replay_maze_avg_distance.append(smooth(mean_maze_distance))
    min_l = min([len(x) for x in replay_maze_avg_distance])
    replay_maze_avg_distance = np.stack([x[:min_l] for x in replay_maze_avg_distance]).mean(axis=0)
    plt.plot(replay_maze_avg_distance, label=f'{folder} ({len(seeds)} seeds)')
plt.legend()
plt.savefig('figures/mean_maze_distance.png')
plt.close()