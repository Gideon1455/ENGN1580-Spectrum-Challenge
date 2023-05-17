import numpy as np
import matplotlib.pyplot as plt

N_BLOCKS = 4
SAMPLES_PER_FRAME = 128
SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
B_PER_FRAME = 4 * N_BLOCKS
ENERGY = (2**12)**2 - 1
freq = 5

phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)

ft = np.fft.fft(phi1)

print(ft[27])
plt.plot(abs(ft))
plt.show()

for i in range(8):
    for j in range(8):
        for k in range(8):
            outputs[i,j,k,:] = np.array(list(temp[i,j,k])).astype(int)