import requests

cid = 'JustinTest'
uid = 'S1'
duration = '15'
noise = '0.1'
frame_width = '1500'
samples = '128'

url = 'http://34.145.212.117/SpectrumChallenge/postCparams.php'

params = {'ADMINID':'Chris',
          'CID': cid, 'DURATION': duration,
          'NOISE': noise,
          'FRAMEWIDTH': frame_width,
          'SAMPLES': samples, 
          'UID': uid}

print(requests.post(url, params=params).text)