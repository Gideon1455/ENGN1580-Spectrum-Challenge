import requests
import time
import re

### PHP functions ############################################################################

def buildChannel(CID,duration,noise,framewidth,samples,users):
    ## Starts channel instance with parameters of choice
    Cparams = {"ADMINID":"Chris",
            "CID":CID,
            "DURATION":duration, # in seconds
            "NOISE":noise,
            "FRAMEWIDTH":framewidth,  # in milliseconds
            "SAMPLES":samples,
            "UID1":users[0],
            "UID2":users[1],
            "UID3":users[2]}
    resp = requests.get(url+"createchannel.php", params=Cparams)
    print("Building channel\n================")
    print(resp.text + "\n")
    return resp

def startChannel(CID,UID):
    ## Destroys channel instance
    resp = requests.get(url+"channelqueue.php", params={"CID":CID,"UID":UID})
    print("Starting channel\n================")
    print(resp.text + "\n")
    return resp

def endChannel(CID):
    ## Destroys channel instance
    resp = requests.get(url+"destroychannel.php", params={"ADMINID":"Chris","CID":CID})
    print("Kill old channel\n================")
    print(resp.text + "\n")
    return resp

def getClock(CID,UID):
    ## Returns: clock CID frame_no time
    resp = requests.get(url+"getclock.php", params={"CID":CID,"UID":UID})
    return resp.text.split()  # returns "[clock, <CID>, <frame no.>, <time>]"

def postS(CID,UID,signal,frame):
    ## Sends signal to channel server at given frame
    """
    Note: 'signal' is a str of hex symbols, every 4 symbols represents 1 UNSIGNED int
    """
    Data = {"CID":CID, "UID":UID, "frame":frame, "signal":signal}
    resp = requests.post(url+"postS.php", params=Data)
    print("Sending signal\n==============")
    print(resp.text + "\n")
    return resp

def getCstatus(CID,UID):
    ## Gets channel state: IDLE, STOP, RUNNING, START
    resp = requests.get(url+"getCstate.php", params={"CID":CID,"UID":UID})
    return resp.text.split()[2]  # returns the STATUS part of the Cstate

def getR(CID,UID):
    ## Returns received signal at current frame ("current" according to channel's clock)
    resp = requests.get(url+"getR.php", params={"CID":CID, "UID":UID})
    data = resp.text.split()

    # Can use below to convert from hex to decimal:
    # R_hex = re.findall("....",resp.split()[2])  # signal in hex, split at every 4 symbols
    # R_dec = [int(x,16) for x in R_hex]  # list of deciaml ints, each up to (2^16 - 1)

    return data[2],data[3]  # frame no., received signal (hex) at current frame

def getB(CID,UID,bytes):
    resp = requests.get(url+"getB.php",params={"CID":CID, "UID":UID, "bytes":bytes})
    return resp.text

##############################################################################################

### Running a channel instance ###############################################################

# Pick channel name!
CID = "CoolChannelBreh"

# Server url
url = "http://34.145.212.117/SpectrumChallenge/"

# Destroy old channel instance (can comment out after starting channel to avoid overhead
endChannel(CID)

# Specify channel users:
Users = ["user1","user2","user3"]  # pick up to 3 usernames
UID = "user2"  # pick a user

# Create channel (can comment out after starting channel to avoid overhead)
buildChannel(CID, duration=15, noise=0.0, framewidth=1000, samples=128, users=Users)

# Queue up (start) channel (clock starts, 'duration' in sec is how long channel runs for)
startChannel(CID,UID)

# Wait till channel status is RUNNING
while True:
    status = getCstatus(CID,UID)
    if status=="RUNNING":
        break

# Create a signal (or use getB.php to generate one)
signal = "8080" * 128  
print("SIGNAL TO SEND IS:",signal,"\n")

# Get frame number and send signal to channel
frame = getClock(CID,UID)[2]
print("Frame from getclock is:",frame,"\n")
resp = postS(CID,UID,signal,frame)

# Print received signals for any number of seconds
start = time.time() 
while True: 
    print(getR(CID,UID))
    if time.time() - start > 1:  # runs for 1s
        break


##############################################################################################

