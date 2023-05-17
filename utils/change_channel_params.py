import requests

cid = 'JustinTest'
uid = 'S1'
duration = '128'
noise = '0'
frame_width = '1000'
samples = '128'

url = 'http://34.145.212.117/SpectrumChallenge/postCparams.php'

params = {'ADMINID':'Chris',
          'CID': cid, 'DURATION': duration,
          'NOISE': noise,
          'FRAMEWIDTH': frame_width,
          'SAMPLES': samples, 
          'UID': uid}

print(requests.post(url, params=params).text)