from sys import path
from os import getcwd

path.append(getcwd() + "/components")
path.append(getcwd() + "/utils")

from channel import Channel # type: ignore
from receiver import Receiver # type: ignore
from transmitter import Transmitter # type: ignore
from utils import dec16_to_hex16, hex16_to_dec16, s_to_arr, arr_to_s

import numpy as np

def start(cid, uid):
    channel = Channel(cid, uid)
    receiver = Receiver(cid, uid)
    SAMPLES_PER_FRAME = 128
    freq = 4

    phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)
    phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)
 
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
                y1 = phi1 * r
                y2 = phi2 * r

                bits = np.zeros(8)
                step = SAMPLES_PER_FRAME // 4
                for i in range(4):
                    bits[2*i] = np.sum(y1[i * step : i * step + step]) >= 0
                    bits[2*i + 1] = np.sum(y2[i * step : i * step + step]) >= 0

                b_hat = hex(int(''.join(bits.astype(int).astype(str)), 2)).split('x')[-1]
                b_hat = '0' * (2 - len(b_hat)) + b_hat

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