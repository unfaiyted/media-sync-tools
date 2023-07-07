from plexapi.server import PlexServer
from plexapi.client import PlexClient
from plexapi.media import Media
import requests
import time
from xml.etree import ElementTree

wait_time = 10

from config import ConfigManager

config = ConfigManager()
plex = config.get_client('plex')

# Get the list of clients
response = requests.get(plex_server + '/clients', headers={'X-Plex-Token': plex_token})

# Parse the XML response
root = ElementTree.fromstring(response.content)

# Extract the clients
clients = [server.attrib for server in root.iter('Server')]

# Print all available clients
for client in clients:
    print('Available client: ', client['name'])

# Define source and target client names
source_client_name = 'faiyts-linux-pc'
target_client_name = 'faiyts-linux-pc'

source_client = None
target_client = None

# Get the list of sessions
sessions = plex.sessions()

for client in clients:
    for session in sessions:
        print('Session: ', session)
        # Check if the client is currently playing a video
        if session.player.machineIdentifier == client['machineIdentifier']:
            if client['name'] == source_client_name:
                metadataId = session.ratingKey
                session.stop("Swapping streams")
                #time.sleep(wait_time)


                media = plex.fetchItem(f'/library/metadata/{metadataId}')


                client = plex.client(source_client_name)

                client.playMedia(media)

                print('Source client found')
                source_client = {
                    'client': client,
                    'session': session
                }
            #elif
            if client['name'] == target_client_name:
                print('Target client found')
                target_client = {
                    'client': client,
                    'session': session
                }

# Check if the source and target clients are found and playing videos
if source_client and target_client:
    # Swap the streams
    print('Swapping streams');
    print('Source client: ', source_client['session'])
    print('Target Media: ', target_client['session'].ratingKey)




    # Fetch the PlexClient objects
    # source_plex_client = plex.client(source_client_name)

    # media = source_client['session'].media[0]
    # print(type(media))
    # print(dir(media))

  #  media.listType = 'video'
  #   if isinstance(media, Media):
  #       print("This object is a Media instance.")
  #   else:
  #       print("This object is not a Media instance.")
    # Swap the streams
    # source_plex_client.playMedia(source_client['session'].media[0])
    metadataId = target_client['session'].ratingKey
    client = plex.client(target_client_name)
    media = plex.fetchItem(metadataId)

    client.stop()
    # target_plex_client.playMedia(media)
else:
    print('Source and/or target client not found or not playing a video.')
