from .components.channel import Channel
from .components.receiver import Receiver
from .components.transmitter import Transmitter
from .utils.utils import dec16_to_hex16, hex16_to_dec16


def start(cid, uid):
    channel = Channel(cid, uid)

    # put whatever you need instantiated before loop starts here

    while True:
        c_state = channel.get_state()
        started = False

        if c_state == 'IDLE':
            # put stuff to do while channel is idle here
            continue

        if c_state == 'START' and not started:
            started = True
            # put stuff to do when channel starts here
            pass

        if c_state == 'RUNNING':
            # put stuff to do when channel is running here
            pass

        if c_state == 'STOP':
            # put stuff to do when channel stops here
            break  # ends while loop


if __name__ == '__main__':
    CID = 'PUT_CHANNEL_ID_HERE'
    UID = 'PUT_USER_ID_HERE'
    start(CID, UID)
