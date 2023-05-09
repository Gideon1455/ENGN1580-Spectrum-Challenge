import requests

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