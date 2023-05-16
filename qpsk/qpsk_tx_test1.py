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
    transmitter = Transmitter(cid, uid)
    sent_frames = []
    SAMPLES_PER_FRAME = 128
    ENERGY = (2**12)**2
    freq = 4

    phi1 = np.sqrt(2) * np.cos(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)
    phi2 = np.sqrt(2) * np.sin(freq * 2 * np.pi * np.arange(SAMPLES_PER_FRAME) / SAMPLES_PER_FRAME)

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
                b = transmitter.get_b(1) # 8 bits, 2 hex chars
                b_str = bin(int(b, 16)).split('b')[-1]
                b_str = '0' * (8 - len(b_str)) + b_str
                bits = np.array([1 if c == '1' else -1 for c in b_str])
                
                extended = np.tile(bits, (SAMPLES_PER_FRAME//4,1)).T
                s1 = phi1 * extended[::2,:].flatten().T
                s2 = phi2 * extended[1::2,:].flatten().T

                to_send = np.round(np.sqrt(ENERGY / 2) * (s1 + s2)).astype(int)
                transmitter.transmit(current_frame, arr_to_s(to_send))
                print(f'sending frame {current_frame}: ' + b_str)
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)