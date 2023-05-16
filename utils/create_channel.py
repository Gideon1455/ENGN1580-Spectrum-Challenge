import requests

cid = 'JustinTest1'
uid1 = 'S1'
uid2 = 'S2'
uid3 = 'S3'
duration = '10'
noise = '0.0'
frame_width = '1000'
samples = '128'

url = 'http://34.145.212.117/SpectrumChallenge/createchannel.php'

params = {'ADMINID':'Chris',
          'CID': cid, 'DURATION': duration,
          'NOISE': noise,
          'FRAMEWIDTH': frame_width,
          'SAMPLES': samples, 
          'UID1': uid1}

print(requests.post(url, params=params).text)