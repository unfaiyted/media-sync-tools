import requests
from urllib.parse import quote_plus
import json

from dotenv import load_dotenv
load_dotenv()

# Plex server details
plex_url = os.getenv('PLEX_SERVER_URL')
plex_token = os.getenv('PLEX_ACCESS_TOKEN')

# The client name
client_name = 'faiyts-linux-pc'

# The headers for authentication
headers = {
    'Accept': 'application/json',
    'X-Plex-Token': plex_token,
}


def printJson(data):
    # check if its a json object already
    if(type(data) == str):
        data = json.loads(data)
    # print(json.dumps(data, indent=4, sort_keys=True))



# Search for The Office
search_url = f'{plex_url}/hubs/search?query=The Office&includeCollections=1'
response = requests.get(search_url, headers=headers)
response.raise_for_status()  # Raise an exception if the request failed

# Find the show
for hub in response.json()['MediaContainer']['Hub']:
    if hub['type'] == 'show':
        for show in hub['Metadata']:
            if show['title'] == 'The Office':
                show_key = show['key']
                break

show_url = f'{plex_url}{show_key}/children'
response = requests.get(show_url, headers=headers)
response.raise_for_status()  # Raise an exception if the request failed

show_data = response.json()
printJson(show_data)  # Print the show data for debugging

# Find the season
for season in show_data['MediaContainer']['Metadata']:
    if 'index' in season and season['index'] == 2:  # Season 2
        season_url = f'{plex_url}{season["key"]}'
        response = requests.get(season_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request failed
        season_data = response.json()
        printJson(season_data)  # Print the season data for debugging

        # Find the episode
        for episode in season_data['MediaContainer']['Metadata']:
            if 'index' in episode and episode['index'] == 3:  # Episode 3
                printJson(episode)  # Print the episode data for debugging
                episode_key = episode['key']
                break



# Get machineIdentifier
response = requests.get(f'{plex_url}/?X-Plex-Token={plex_token}', headers=headers)
response.raise_for_status()
data = response.json()
machineIdentifier = data['MediaContainer']['machineIdentifier']

# print(machineIdentifier)




headers = {
    'Accept': 'application/json',
    'X-Plex-Target-Client-Identifier': machineIdentifier,
    'X-Plex-Token': plex_token
}

# Start playback on the client
playback_url = f'{plex_url}/player/playback/playMedia?protocol=https&address=plex.faiyts.media&port=443&commandID=0'
playback_url += f'&key={quote_plus(episode_key)}'
playback_url += f'&machineIdentifier={machineIdentifier}'

response = requests.get(playback_url, headers=headers)
response.raise_for_status()  # Raise an exception if the request failed


print('Playback started successfully.')
