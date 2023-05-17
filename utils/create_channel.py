import requests

cid = 'JustinTest2'
uid1 = 'S1'
uid2 = 'S2'
uid3 = 'S3'
duration = '20'
noise = '0.02'
frame_width = '2000'
samples = '128'

url = 'http://34.145.212.117/SpectrumChallenge/createchannel.php'

params = {'ADMINID':'Chris',
          'CID': cid, 'DURATION': duration,
          'NOISE': noise,
          'FRAMEWIDTH': frame_width,
          'SAMPLES': samples, 
          'UID1': uid1,
          'UID2': uid2}

print(requests.post(url, params=params).text)