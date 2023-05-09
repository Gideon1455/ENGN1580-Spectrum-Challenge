import requests

##########################################################################################
# Receiver-specific functions ############################################################
##########################################################################################
CID = "MilesChannel"
UID = "user2"
url = "http://34.145.212.117/SpectrumChallenge/"

def getClock(CID,UID):
    ## Returns: clock CID frame_no time
    resp = requests.get(url+"getclock.php", params={"CID":CID,"UID":UID})
    return resp.text.split()  # returns "[clock, <CID>, <frame no.>, <time>]"

def getCstatus(CID,UID):
    ## Gets channel state: IDLE, STOP, RUNNING, START
    resp = requests.get(url+"getCstate.php", params={"CID":CID,"UID":UID})
    return resp.text.split()[2]  # returns the STATUS part of the Cstate

def getR(CID,UID):
    ## Returns received signal at current frame ("current" according to channel's clock)
    resp = requests.get(url+"getR.php", params={"CID":CID, "UID":UID})
    data = resp.text.split()  
    return data[-1]  # data = ['R',CID,frame,signal] (signal in hex)

def postB(CID,UID,bhat):
    resp = requests.get(url+"postBhat.php", params={"CID":CID, "UID":UID,"bhat":bhat})
    return resp.text

##########################################################################################
# Receive and decode signal ##############################################################
##########################################################################################

seen_frames = []
while True:
    status = getCstatus(CID,UID)
    if status=="RUNNING":
        try:
            frame = int(getClock(CID,UID)[2])  # will skip rest of loop if not int
        except (IndexError, ValueError):
            continue
        if frame not in seen_frames and frame > 0:
            # BELOW DEPENDS ON YOUR DECODING SCHEME:
            # Get signal from channel, convert to binary (1 hex = 4 bits)
            signal = getR(CID,UID)
            bits = ''
            for i in range(0, len(signal), 4):
                hx_to_int = int(signal[i:i+4],16)
                bits += '0' if hx_to_int < 2**15 else '1'
            
            # convert back to original hex and post to server
            bhat = ''
            for i in range(0, len(bits), 4):
                bhat += hex(int(bits[i:i+4], 2)).split('x')[-1]

            seen_frames.append(frame)

            # for show and tell, can print received signal
            print("bits received:",frame,bhat,"\n")

    elif status=="STOP":
        print("Channel is stopped\n")
        break

##########################################################################################