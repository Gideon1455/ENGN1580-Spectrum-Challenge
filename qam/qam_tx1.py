from sys import path
from os import getcwd

path.append(getcwd() + "/components")
path.append(getcwd() + "/utils")

from channel import Channel # type: ignore
from receiver import Receiver # type: ignore
from transmitter import Transmitter # type: ignore
from utils import dec16_to_hex16, hex16_to_dec16, s_to_arr, arr_to_s

import numpy as np
import matplotlib.pyplot as plt

def start(cid, uid):
    channel = Channel(cid, uid)
    transmitter = Transmitter(cid, uid)
    sent_frames = []
    N_BLOCKS = 4
    SAMPLES_PER_FRAME = 128
    SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
    ENERGY = (2**12)**2
    freq = 1

    phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
    phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)

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
                b_per_frame = 16
                b = transmitter.get_b(b_per_frame / 8) # 8 bits, 2 hex chars
                b_str = bin(int(b, 16)).split('b')[-1]
                b_str = '0' * (b_per_frame - len(b_str)) + b_str
                
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
        
                to_send = np.round(np.sqrt(8 * ENERGY / 9) * s_blocks.flatten()).astype(int)
                print(arr_to_s(to_send))
                plt.plot(to_send)
                plt.title('tx')
                plt.show()
                transmitter.transmit(current_frame, arr_to_s(to_send))
                print(f'sending frame {current_frame}: ' + b_str)
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)