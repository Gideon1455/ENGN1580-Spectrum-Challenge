from sys import path
from os import getcwd

path.append(getcwd() + "/components")
path.append(getcwd() + "/utils")

from channel import Channel # type: ignore
from receiver import Receiver # type: ignore
from transmitter import Transmitter # type: ignore
from utils import dec16_to_hex16, hex16_to_dec16, s_to_arr, arr_to_s, int_to_bin
from generate_phis import generate_phi_pair # type: ignore
from gray_code import gray_code # type: ignore

import numpy as np

def start(cid, uid):
    channel = Channel(cid, uid)
    receiver = Receiver(cid, uid)
    N_BLOCKS = 32
    SAMPLES_PER_FRAME = 128
    SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
    B_PER_BLOCK = 9
    B_PER_FRAME = B_PER_BLOCK * N_BLOCKS
    ENERGY = (2**12)**2 / 0.5

    phis = np.vstack((np.ones(SAMPLES_PER_BLOCK), generate_phi_pair(SAMPLES_PER_BLOCK, SAMPLES_PER_BLOCK)))
    i_to_bin_vectorized = np.vectorize(lambda x: int_to_bin(x, B_PER_BLOCK))
    grid = i_to_bin_vectorized(np.arange(8**3).reshape((8,8,8)))
    
    seen_frames = []

    while True:
        c_state = channel.get_state()
        started = False

        if c_state == 'IDLE':
            continue

        if c_state == 'START' and not started:
            started = True
            seen_frames = []

        if c_state == 'RUNNING':
            try:
                current_frame, signal = channel.get_output()
            except RuntimeError:
                continue

            if current_frame not in seen_frames:
                r = s_to_arr(signal)

                bits = np.zeros(B_PER_FRAME)
                for i, idx in enumerate(range(0, r.size, SAMPLES_PER_BLOCK)):
                    r_slice = r[idx:idx+SAMPLES_PER_BLOCK]
                    ys = phis * r_slice
                    amps = np.sum(ys, 1) / np.sqrt(ENERGY / 2.3) / SAMPLES_PER_BLOCK

                    boundaries = [-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]
                    phi_divs = np.zeros((len(phis), len(boundaries) + 1))

                    for j, boundary in enumerate(boundaries):
                        if i == 0:
                            phi_divs[:, j] = amps < boundary
                        else:
                            phi_divs[:, j] = (amps < boundary) & (amps >= boundaries[j-1])

                    phi_divs[:, -1] = amps >= boundaries[-1]

                    x,y,z = np.argmax(phi_divs,1)
                    bits[B_PER_BLOCK*i:B_PER_BLOCK*(i+1)] = list(grid[x,y,z])
                
                b_hat = hex(int(''.join(bits.astype(int).astype(str)), 2)).split('x')[-1]
                b_hat = '0' * (B_PER_FRAME // 4 - len(b_hat)) + b_hat

                receiver.post_b_hat(b_hat)
                print(f'received frame {current_frame}: ' + ''.join(bits.astype(int).astype(str)))
                seen_frames.append(current_frame)

        if c_state == 'STOP':
            _, sent, errors = channel.get_my_score()
            print(f'Total sent: {sent}, Total errors: {errors}')
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)