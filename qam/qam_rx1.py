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
    receiver = Receiver(cid, uid)
    N_BLOCKS = 4
    SAMPLES_PER_FRAME = 128
    SAMPLES_PER_BLOCK = SAMPLES_PER_FRAME // N_BLOCKS
    ENERGY = (2**12)**2
    freq = 1

    phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
    phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_BLOCK) / SAMPLES_PER_BLOCK)
 
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
                b_per_frame = 16
                r = s_to_arr(signal)

                bits = np.zeros(b_per_frame)
                for i, idx in enumerate(range(0, r.size, SAMPLES_PER_BLOCK)):
                    r_slice = r[idx:idx+SAMPLES_PER_BLOCK]
                    y1 = phi1 * r_slice
                    y2 = phi2 * r_slice
                    amp1 = np.sum(y1) / np.sqrt(8 * ENERGY / 9) / SAMPLES_PER_BLOCK
                    amp2 = np.sum(y2) / np.sqrt(8 * ENERGY / 9) / SAMPLES_PER_BLOCK
                    ang = abs(np.rad2deg(np.arctan(amp2/amp1)))

                    bits[4*i] = 0 if amp1 > 0 else 1
                    bits[4*i+1] = 0 if amp2 > 0 else 1
                    
                    if abs(amp1) > 0.5 and abs(amp2) > 0.5:
                        bits[4*i+2] = 1
                        bits[4*i+3] = 1
                    elif abs(amp1) < 0.5 and abs(amp2) < 0.5:
                        bits[4*i+2] = 0
                        bits[4*i+3] = 0
                    else:
                        bits[4*i+2] = 1 if ang > 45 else 0
                        bits[4*i+3] = 1 if ang < 45 else 0

                b_hat = hex(int(''.join(bits.astype(int).astype(str)), 2)).split('x')[-1]
                b_hat = '0' * (4 - len(b_hat)) + b_hat

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