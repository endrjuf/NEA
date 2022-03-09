import requests

authKey = '3348883f28df463b9fe41079aa10b7af'

headers = {
    'authorization': authKey,
    'content-type': 'application/json'
}

response = requests.get(
    url= "https://api.assemblyai.com/v2/transcript/ozyi3xmkym-5a75-490e-a88b-758982761736",
    headers= headers
)

json = response.json()

x = json['audio_duration']
print(x)