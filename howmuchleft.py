import requests
from extract import json_extract
import datetime


authKey = '39e03013f79342708b140a7f4668a0cd'

headers = {
    'authorization': authKey,
    'content-type': 'application/json'
}

def getids():
    response = requests.get(
        url= "https://api.assemblyai.com/v2/transcript?limit=200&status=completed",
        headers= headers
    )

    json = response.json()

    ids = json_extract(json, 'id')

    counting(ids)

def counting(ids):
    time = 0
    for x in range(0, len(ids)):
        response = requests.get(
            url="https://api.assemblyai.com/v2/transcript/"+ids[x],
            headers=headers
        )
        json = response.json()
        y = json['audio_duration']
        time += y
        print(time)
    timesis = str(datetime.timedelta(seconds=time))
    print(f'Time used of transcription is:{timesis}')

getids()


