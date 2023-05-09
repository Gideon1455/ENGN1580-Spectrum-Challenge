from channel import Channel
from receiver import Receiver
from transmitter import Transmitter
from utils import dec16_to_hex16, hex16_to_dec16

def start(cid, uid):
    channel = Channel(cid, uid)
    receiver = Receiver(cid, uid)

    seen_frames = None

    while True:
        c_state = channel.get_state()
        started = False

        if c_state == 'IDLE':
            continue

        if c_state == 'START' and not started:
            started = True
            _, _, _, samples_per_frame = channel.get_params()
            seen_frames = []

        if c_state == 'RUNNING':
            try:
                current_frame, signal = channel.get_output()
            except RuntimeError:
                continue

            if current_frame not in seen_frames:
                bits = ''
                for i in range(0, len(signal), 4):
                    bits += '0' if hex16_to_dec16(signal[i:i+4]) < 0 else '1'
                print(bits)
                b_hat = ''
                for i in range(0, len(bits), 4):
                    b_hat += hex(int(bits[i:i+4], 2)).split('x')[-1]

                receiver.post_b_hat(b_hat)
                print(f'received frame {current_frame}')
                seen_frames.append(current_frame)

        if c_state == 'STOP':
            _, sent, errors = channel.get_score()
            print(f'Total sent: {sent}, Total errors: {errors}')
            break

if __name__ == '__main__':
    CID = 'JustinTest'
    UID = 'S1'
    start(CID, UID)