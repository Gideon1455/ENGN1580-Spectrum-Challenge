from sys import path
from os import getcwd

path.append(getcwd() + "/components")
path.append(getcwd() + "/utils")

from channel import Channel # type: ignore
from receiver import Receiver # type: ignore
from transmitter import Transmitter # type: ignore
from utils import dec16_to_hex16, hex16_to_dec16

def start(cid, uid):
    channel = Channel(cid, uid)
    transmitter = Transmitter(cid, uid)

    samples_per_frame = None
    sent_frames = []

    while True:
        c_state = channel.get_state()
        started = False

        if c_state == 'IDLE':
            continue

        if c_state == 'START' and not started:
            started = True
            _, _, _, samples_per_frame = channel.get_params()
            sent_frames = []

        if c_state == 'RUNNING':
            try:
                current_frame, _ = channel.get_clock()
            except RuntimeError:
                continue

            if current_frame not in sent_frames:
                b = transmitter.get_b(samples_per_frame / 8) # 8 bits, 2 hex chars
                bits = bin(int(b, 16)).split('b')[-1]
                bits = '0' * (128 - len(bits)) + bits

                to_send = ''
                for bit in bits:
                    to_send += '7FFF' if bit == '0' else '8001'
                
                transmitter.transmit(current_frame, to_send)
                print(f'sending frame {current_frame}')
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            _, sent, errors = channel.get_score()
            print(f'Total sent: {sent}, Total errors: {errors}')
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)