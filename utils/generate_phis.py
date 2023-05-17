import numpy as np
import matplotlib.pyplot as plt

def generate_phi_pair(interval_len, period):
    n_periods = interval_len // period;
    phi1 = np.ones(period)
    phi2 = np.ones(period)
    phi1[period//2:] = -1
    phi2[:period//4] = -1
    phi2[3*period//4:] = -1
    
    phi1 = np.tile(phi1, n_periods)
    phi2 = np.tile(phi2, n_periods)
    
    return np.vstack((phi1, phi2))