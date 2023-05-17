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
    B_PER_BLOCK = 9
    B_PER_FRAME = B_PER_BLOCK * N_BLOCKS
    ENERGY = (2**12)**2

    phis = np.vstack((np.ones(SAMPLES_PER_BLOCK), generate_phi_pair(SAMPLES_PER_BLOCK, SAMPLES_PER_BLOCK)))
    i_to_bin_vectorized = np.vectorize(lambda x: int_to_bin(x, B_PER_BLOCK))
    grid = i_to_bin_vectorized(np.arange(8**3).reshape((8,8,8)))

    to_block = []
    seen = []
    
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

            
            if current_frame == 0 or current_frame == 1 or current_frame == 2:
                if (current_frame == 1 or current_frame == 2) and current_frame not in seen:
                    try:
                        to_block.append(int(transmitter.get_receiver_state()))
                        seen.append(current_frame)
                    except:
                        print('ohno')
                continue

            if current_frame not in sent_frames:
                b = transmitter.get_b(B_PER_FRAME // 8) # 8 bits, 2 hex chars
                b_str = bin(int(b, 16)).split('b')[-1]
                b_str = '0' * (B_PER_FRAME - len(b_str)) + b_str
                
                s_blocks = np.zeros((N_BLOCKS, SAMPLES_PER_BLOCK))
                for i, idx in enumerate(range(0, len(b_str), B_PER_BLOCK)):
                    str_slice = b_str[idx:idx+B_PER_BLOCK]

                    amp2_grid, amp1_grid, amp3_grid = np.meshgrid([-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875],
                                                                  [-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875],
                                                                  [-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875])

                    amp1, amp2, amp3 = amp1_grid[grid == str_slice][0], amp2_grid[grid == str_slice][0], amp3_grid[grid == str_slice][0]

                    s_blocks[i] = np.sum(np.expand_dims(np.array([amp1,amp2,amp3]),1) * phis, 0)
        

                if len(to_block) > 0:
                    freq = np.mean(to_block)
                    if abs(freq - 0) > 3 and abs(freq - N_BLOCKS) > 3:
                        jam1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)
                        jam2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)
                        to_send = np.round(np.sqrt(ENERGY / 2.3) * s_blocks.flatten()).astype(int)
                        to_send = np.round(np.sqrt(ENERGY / 2.1) * (jam1 + jam2)).astype(int)
                        
                    else:
                        to_send = np.round(np.sqrt(ENERGY / 2.3) * s_blocks.flatten()).astype(int)
                else:
                    to_send = np.round(np.sqrt(ENERGY / 2.3) * s_blocks.flatten()).astype(int)

                print(np.sum(np.square(to_send)) / SAMPLES_PER_FRAME)
                transmitter.transmit(current_frame, arr_to_s(to_send))
                print(f'sending frame {current_frame}: ' + b_str)
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            break

if __name__ == '__main__':
    CID = 'JustinTest2'
    UID = 'S1'
    start(CID, UID)