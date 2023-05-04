import requests
import re

##########################################################################################
# Transmitter-specific functions #########################################################
##########################################################################################
CID = "MilesChannel"
UID = "user2"
url = "http://34.145.212.117/SpectrumChallenge/"

def getClock(CID,UID):
    ## Returns: clock CID frame_no time
    resp = requests.get(url+"getclock.php", params={"CID":CID,"UID":UID})
    return resp.text.split()  # returns "[clock, <CID>, <frame no.>, <time>]"

def postS(CID,UID,signal,frame):
    ## Sends signal to channel server at given frame
    """
    Note: 'signal' is a str of hex symbols, every 4 symbols represents 1 int
    """
    Data = {"CID":CID, "UID":UID, "frame":frame, "signal":signal}
    resp = requests.post(url+"postS.php", params=Data)
    print("Sending signal at frame",frame)
    print("status code:",resp.status_code,"\n")
    return resp

def getCstatus(CID,UID):
    ## Gets channel state: IDLE, STOP, RUNNING, START
    resp = requests.get(url+"getCstate.php", params={"CID":CID,"UID":UID})
    return resp.text.split()[2]  # returns the STATUS part of the Cstate

# def getB(CID,UID,bytes):
#     resp = requests.get(url+"getB.php",params={"CID":CID, "UID":UID, "bytes":bytes})
#     return resp.text.split()[-1]

def getB(CID,UID,bytes):
    """Gets bits for transmission.
    
    :param bytes: number of bytes to pull
    :type bytes: int
    :return: hex string representing bits to transmit
    :rtype: str
    """
    req = requests.get(url + "getB.php", params={'CID':CID,'UID':UID,'bytes':bytes})
    return re.search("^HEX: (.*)$", req.text.rstrip()).group(1)

##########################################################################################
# Encode signal and send to channel ######################################################
##########################################################################################
sent_frames = []
while True:
    status = getCstatus(CID,UID)
    if status=="RUNNING":
        try:
            frame = getClock(CID,UID)[2]
        except IndexError:
            continue
        if frame not in sent_frames:
            # Get hex from server, convert to binary (1 hex = 4 bits)
            try:
                b = getB(CID,UID,128/8)
            except:
                continue
            bits = bin(int(b, 16)).split('b')[-1]
            bits = '0' * (128 - len(bits)) + bits  # zero padding

            # Example encoding scheme (not necessarily a good one!!):
            """
            Note: 
            0x8000 = hex(2**15)
            0x7c00 = hex(2**15 - 2**10) (encoding 0)
            0x8400 = hex(2**15 + 2**10) (encoding 1)

            1 hex --> 4 bits --> 16 hex (below each bit gets 4 hex)
            """
            signal = ''
            for bit in bits:
                signal += "7c00" if bit=="0" else "8400"  

            # send signal
            postS(CID,UID,signal,frame)    
            sent_frames.append(frame)

            # for show and tell, can print signal sent
            print("sent signal:",frame,b,"\n")

    elif status=="STOP":
        print("Channel is stopped\n")
        break

##########################################################################################