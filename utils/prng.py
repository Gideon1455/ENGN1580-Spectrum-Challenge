import numpy as np

def generate(seed, number_of_bits):
    seed = tuple(map(lambda x: int(x), tuple(bin(seed).split("b")[-1])))
    seed = np.array(seed)
    if len(seed) > 31: seed = seed[:31]
    if len(seed) < 31: seed = np.pad(seed, (31 - len(seed), 0))

    seed = list(seed)
    seed.reverse()
    output = []
    for _ in range(number_of_bits):
        tap1, tap2 = seed[27], seed[30]
        new_value = tap1 ^ tap2
        output.append(seed.pop(-1))
        seed.insert(0, new_value)
    
    return output
