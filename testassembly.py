import requests
import time

#########################################################

authKey = '3348883f28df463b9fe41079aa10b7af'


headers = {
    'authorization': authKey,
    'content-type': 'application/json'
}

uploadUrl = 'https://api.assemblyai.com/v2/upload'
transcriptUrl = 'https://api.assemblyai.com/v2/transcript'
#########################################################
def uploadMyFile(fileName):

    def _readmyFile(fn):

        chunkSize = 5242880

        with open(fn, "rb") as fileStream:

            while True:
                data = fileStream.read(chunkSize)

                if not data:
                    break

                yield data

    response = requests.post(
        uploadUrl,
        headers=headers,
        data=_readmyFile(fileName)

    )

    json = response.json()

    return json['upload_url']

def startTranscription(aurl):

    response = requests.post(
        transcriptUrl,
        headers=headers,
        json={'audio_url': aurl}
    )

    json = response.json()

    return json['id']

def getTranscription(tid):

    maxAttempts = 50
    timedout = False

    while True:
        response = requests.get(
            f'{transcriptUrl}/{tid}',
            headers=headers
        )

        json = response.json()

        if json['status'] == 'completed':
            break

        maxAttempts -= 1
        timedout = maxAttempts <= 0

        print(maxAttempts)

        if timedout:
            break

        time.sleep(3)

    return 'Timed out...' if timedout else json['text']

#########################################################

audioUrl = uploadMyFile('Adele Hello lyrics.mp3')

#########################################################

transcriptionID = startTranscription(audioUrl)

#########################################################

text = getTranscription(transcriptionID)

print(f'Result: {text}')