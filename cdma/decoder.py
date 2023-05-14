from sys import path
from os import getcwd

path.append(getcwd() + "/utils")

import numpy as np
from prng import generate # type: ignore

clen = 128
c = np.array(generate(140256304, clen))
c[c==0] = -1

with open("CDMA128_2023.txt", "r") as f:
    lines = f.readlines()

Q = np.array([list(map(lambda x: int(x), l)) for l in [line.strip().split() for line in lines]])
m = np.matmul(Q,c) > 0

mystr = ''
for i in range(0, len(m), 7):
    bits = int(''.join(map(lambda x: str(int(x)), m[i:i+7])))
    mystr += chr(bits)

print(mystr)