import sys
import requests
import re
import numpy as np

class Channel:
    """Represents a channel.
    """
    def __init__(self, cid, uid, url="http://34.145.212.117/SpectrumChallenge/"):
        """Constructor for a channel.
        
        :param cid: channel ID
        :type cid: str
        :param uid: user ID
        :type uid: str
        :param url: server url,
            defaults to http://34.145.212.117/SpectrumChallenge/
        :type url: str
        :return: None
        """
        self.cid = cid
        self.uid = uid
        self.url = url
        self.GET_CLOCK = 'getclock.php'
        self.GET_R = 'getR.php'
        self.GET_C_PARAMS = 'getCparams.php'
        self.GET_C_STATE = 'getCstate.php'
        self.GET_C_SCORE = 'getCscore.php'
        self.GET_MY_SCORE = 'getMYscore.php'


    def get_clock(self):
        """Returns the current frame number and time for the channel.

        :return: A tuple of the current frame number and the current time
        :rtype: tuple(int, float)
        :raises Exception: indicates trouble with channel clock file
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.get(self.url + self.GET_CLOCK, params=params)

        try:
            _, _, frame_number, time = req.text.split()
            return int(frame_number), float(time)
        except ValueError:
            raise RuntimeError('Trouble with channel output file')


    def get_output(self):
        """Returns the channel output on the current frame.

        :return: A tuple of the current frame number and the channel output in hex
        :rtype: tuple(int, str)
        :raises Exception: indicates trouble with channel output file
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.get(self.url + self.GET_R, params=params)
        try:
            _, _, frame_number, signal = req.text.split()
            return int(frame_number), signal
        except ValueError:
            raise RuntimeError('Trouble with channel output file')


    def get_params(self):
        """Returns the channel parameters.

        :return: A tuple of the channel duration, noise, frame width, and samples per frame
        :rtype: tuple(int, float, int, int)
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.get(self.url + self.GET_C_PARAMS, params=params)
        _, duration, noise, frame_width, samples = req.text.split()
        return int(duration), float(noise), int(frame_width), int(samples)


    def get_state(self):
        """Returns the channel state.

        :return: The channel state ("IDLE", "START", "RUNNING", "STOP")
        :rtype: str
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.get(self.url + self.GET_C_STATE, params=params)
        try:
            _, _, state = req.text.split()
        except:
            state = ''
        return state
    

    def get_my_score(self):
        """Gets current score.

        :return: frame number, cumulative bits sent, cumulative errors
        :rtype: tuple(int, int, int)
        """
        params = {'UID': self.uid, 'CID': self.cid}
        req = requests.get(self.url + self.GET_MY_SCORE, params=params)
        frame_number, sent, errors = re.search(f"score ([0-9]+ [0-9]+ [0-9]+)", req.text).group(1).split()
        return int(frame_number), int(sent), int(errors)

class Receiver:
    """Represents a receiver.
    """
    def __init__(self, cid, uid, url="http://34.145.212.117/SpectrumChallenge/"):
        """Constructor for a receiver.
        
        :param cid: channel ID
        :type cid: str
        :param uid: user ID
        :type uid: str
        :param url: server url,
            defaults to http://34.145.212.117/SpectrumChallenge/
        :type url: str
        :return: None
        """
        self.cid = cid
        self.uid = uid
        self.url = url
        self.POST_X_STATE = 'postXstate.php'
        self.POST_B_HAT = 'postBhat.php'
        self.GET_B_HAT = 'gettBhat.php'

    def post_state(self, state):
        """Posts a receiver state.
        
        :param state: state of the receiver
        :type state: str
        :return: post request status code
        :rtype: int
        """
        params = {'CID': self.cid, 'UID': self.uid, 'state': state}
        req = requests.post(self.url + self.POST_X_STATE, params=params)
        return req.status_code
    
    def post_b_hat(self, b_hat):
        """Posts reconstructed signal (b hat).
        
        :param b_hat: reconstructed signal in hex
        :type b_hat: str
        :return: post request status code
        :rtype: int
        """
        params = {'CID': self.cid, 'UID': self.uid, 'bytes': b_hat}
        req = requests.post(self.url + self.POST_B_HAT, params=params)
        return req.status_code
    
    def get_b_hat(self):
        """Gets reconstructed signal (b hat).
        
        :return: reconstructed signal
        :rtype: str
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.post(self.url + self.POST_B_HAT, params=params)
        return req.status_code


class Transmitter():
    """Represents a transmitter.
    """
    def __init__(self, cid, uid, url="http://34.145.212.117/SpectrumChallenge/"):
        """Constructor for a transmitter.
        
        :param cid: channel ID
        :type cid: str
        :param uid: user ID
        :type uid: str
        :param url: server url,
            defaults to http://34.145.212.117/SpectrumChallenge/
        :type url: str
        :return: None
        """
        self.cid = cid
        self.uid = uid
        self.url = url
        self.POST_S = 'postS.php'
        self.GET_X_STATE = 'getXstate.php'
        self.GET_B = 'getB.php'

    def transmit(self, frame, signal):
        """Transmits a signal to a channel.

        :param frame: frame number to post the signal to
        :type frame: int
        :param signal: signal to post
        :type signal: str
        :return: post request status code
        :rtype: int
        """
        params = {'CID': self.cid, 'UID': self.uid, 'frame': frame, 'signal': signal}
        req = requests.post(self.url + self.POST_S, params=params)
        return req.status_code
    
    def get_receiver_state(self):
        """Returns the receiver state.

        :return: receiver state
        :rtype: str
        """
        params = {'CID': self.cid, 'UID': self.uid}
        req = requests.get(self.url + self.GET_X_STATE, params=params)
        return re.search("^XSTATE: \w+ \w+ (.*)$", req.text.rstrip()).group(1)

    def get_b(self, bytes):
        """Gets bits for transmission.
        
        :param bytes: number of bytes to pull
        :type bytes: int
        :return: hex string representing bits to transmit
        :rtype: str
        """
        params = {'CID': self.cid, 'UID': self.uid, 'bytes': bytes}
        req = requests.get(self.url + self.GET_B, params=params)
        return re.search("^HEX: (.*)$", req.text.rstrip()).group(1)

def generate_phi_pair(interval_len, period):
    n_periods = interval_len // period;
    phi1 = np.ones(period)
    phi2 = np.ones(period)
    phi1[period//2:] = -1
    phi2[:period//4] = -1
    phi2[3*period//4:] = -1
    
    phi1 = np.tile(phi1, n_periods)
    phi2 = np.tile(phi2, n_periods)
    
    return np.vstack((phi1, phi2))

def dec16_to_hex16(value: int) -> str:
    temp = hex(value + 32768)
    temp = '0' * (4 - len(temp)) + temp
    return temp.split('x')[-1]

def hex16_to_dec16(value: str) -> int:
    return int(value, 16) - 32768

def arr_to_s(arr) -> str:
    f = np.vectorize(dec16_to_hex16)
    return ''.join(f(arr))

def s_to_arr(s):
    out = np.zeros(len(s) // 4)
    for i in range(out.size):
        out[i] = hex16_to_dec16(s[4*i: 4*i + 4])
    return out

def int_to_bin(i, l):
    b = bin(i).split('b')[-1]
    b = '0' * (l - len(b)) + b
    return b

def start(cid, uid, url):
    channel = Channel(cid, uid, url)
    transmitter = Transmitter(cid, uid, url)
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
                transmitter.transmit(current_frame, arr_to_s(to_send))
                print(f'sending frame {current_frame}: ' + b_str)
                sent_frames.append(current_frame)

        if c_state == 'STOP':
            break

if __name__ == '__main__':
    CID = sys.argv[1]
    UID = sys.argv[2]
    ip = sys.argv[3]
    url=f'http://{ip}/SpectrumChallenge/'
    start(CID, UID, url)