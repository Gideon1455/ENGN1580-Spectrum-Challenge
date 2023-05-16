import requests
import re

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
        _, _, state = req.text.split()
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
