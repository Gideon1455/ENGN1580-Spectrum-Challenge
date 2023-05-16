import numpy as np

def dec16_to_hex16(value: int) -> str:
    temp = hex(value + 32768)
    temp = '0' * (4 - len(temp)) + temp
    return temp.split('x')[-1]

def hex16_to_dec16(value: str) -> int:
    return int(value, 16) - 32768

def arr_to_s(arr) -> str:
    f = np.vectorize(dec16_to_hex16)
    return ''.join(f(arr))

def s_to_arr(s):
    out = np.zeros(len(s) // 4)
    for i in range(out.size):
        out[i] = hex16_to_dec16(s[4*i: 4*i + 4])
    return out