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
    transmitter = Transmitter(cid, uid)
    sent_frames = []
    N_BLOCKS = 32
    SAMPLES_PER_FRAME = 128
    SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
    B_PER_BLOCK = 2
    B_PER_FRAME = B_PER_BLOCK * N_BLOCKS
    ENERGY = (2**12)**2 / 1.000132

    phis = generate_phi_pair(SAMPLES_PER_BLOCK, SAMPLES_PER_BLOCK)

    while True:
        c_state = channel.get_state()
        started = False

        if c_state == 'IDLE':
            continue

        if c_state == 'START' and not started:
            started = True

        if c_state == 'RUNNING':
            try:
                current_frame, _ = channel.get_clock()
            except RuntimeError:
                continue

            if current_frame not in sent_frames:
                b = transmitter.get_b(B_PER_FRAME // 8) # 8 bits, 2 hex chars
                b_str = bin(int(b, 16)).split('b')[-1]
                b_str = '0' * (B_PER_FRAME - len(b_str)) + b_str
                bits = np.array([1 if c == '1' else -1 for c in b_str])

                s_blocks = np.zeros((N_BLOCKS, SAMPLES_PER_BLOCK))
                
                for i in range(N_BLOCKS):
                    s_blocks[i] = np.sum(phis * np.expand_dims(bits[B_PER_BLOCK*i:B_PER_BLOCK*(i+1)],1), 0)

                to_send = np.round(np.sqrt(ENERGY / 2) * s_blocks.flatten()).astype(int)
                print(np.sum(np.square(to_send)) / 128)
                transmitter.transmit(current_frame, arr_to_s(to_send))
                print(f'sending frame {current_frame}: ' + b_str)
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)