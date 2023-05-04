import requests
import re

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
