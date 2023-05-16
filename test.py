import numpy as np
import matplotlib.pyplot as plt
N_BLOCKS = 4
SAMPLES_PER_FRAME = 128
SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
ENERGY = (2**12)**2
freq = 1

phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
b_str = '0010101110100000'
s_blocks = np.zeros((N_BLOCKS, SAMPLES_PER_BLOCK))
for i, idx in enumerate(range(0, len(b_str), 4)):
    str_slice = b_str[idx:idx+4]

    if str_slice[-2:] == '00':
        amp1 = 0.25
        amp2 = 0.25
    elif str_slice[-2:] == '01':
        amp1 = 0.75
        amp2 = 0.25
    elif str_slice[-2:] == '10':
        amp1 = 0.25
        amp2 = 0.75
    else:
        amp1 = 0.75
        amp2 = 0.75
    
    if str_slice[0] == '1':
        amp1 = -amp1
    
    if str_slice[1] == '1':
        amp2 = -amp2
    
    s_blocks[i] = amp1 * phi1 + amp2 * phi2

plt.plot(np.round((ENERGY/2) * s_blocks.flatten()).astype(int))
plt.show()