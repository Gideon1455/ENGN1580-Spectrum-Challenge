from sys import path
from os import getcwd

path.append(getcwd() + "/utils")

import numpy as np
from pnsg import generate # type: ignore

seed = 1 # < PUT YOUR ID HERE (REPLACE THE 1 WITH YOUR ID) >
nbits = 128

with open("CDMA128_2023.txt", "r") as f:
    lines = f.readlines()

Q = np.array([list(map(lambda x: int(x), l)) for l in [line.strip().split() for line in lines]])

S = np.array(generate(seed, len(lines) * nbits)).reshape((len(lines), nbits))
S[S==0] = -1

m = np.sum(Q * S, 1) > 0
mystr = ''
for i in range(0, len(m), 7):
    bits = np.flip(m[i:i+7])
    bits = ''.join(map(lambda x: str(int(x)), bits))
    mystr += chr(int(bits, 2))

print(mystr)