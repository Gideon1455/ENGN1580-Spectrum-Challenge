from sys import path
from os import getcwd

path.append(getcwd() + "/utils")

import numpy as np
from pnsg import generate # type: ignore

seed = 1 # < PUT YOUR ID HERE (REPLACE THE 1 WITH YOUR ID) >
frame_width = 128

with open("CDMA128_2023.txt", "r") as f:
    lines = f.readlines()

Q = np.array([list(map(lambda x: int(x), l)) for l in [line.strip().split() for line in lines]])
 
S = np.array(generate(seed, len(lines) * frame_width)).reshape((len(lines), frame_width))
S[S==0] = -1

b_hat = np.sum(Q * S, 1) > 0
message = ''
for i in range(0, len(b_hat), 7):
    bit_string = ''.join(map(lambda x: str(int(x)), np.flip(b_hat[i:i+7])))
    message += chr(int(bit_string, 2))

print(message)