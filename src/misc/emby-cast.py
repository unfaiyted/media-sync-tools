import embypy

# Replace these with your Emby server URL and API key

EMBY_SERVER_URL = 'https://emby.faiyts.media'
EMBY_API_KEY = os.getenv('EMBY_API_KEY')

username = 'Faiyt'

# Initialize the Emby API client
emby_client = embypy.Emby(EMBY_SERVER_URL, EMBY_API_KEY)

# You would typically authenticate, either by username and password or by using an API key
# emby_client.authenticate("YOUR_EMBY_USERNAME", "YOUR_EMBY_PASSWORD")

# Fetch items from Emby library
items = emby_client.items()

# Look for the first episode of The Office
episode_id = None
for item in items:
    if item.type == "Episode" and "The Office" in item.name and "S01E01" in item.name:
        episode_id = item.id
        break

# If the episode is found, attempt to play it on all devices
if episode_id:
    # Fetch the list of devices
    devices = emby_client.devices()

    # Construct the play command payload
    play_command = {
        "ItemIds": [episode_id],
        "PlayCommand": "PlayNow"
    }

    # Send the play command to each device
    for device in devices:
        device_id = device['Id']
        emby_client.sessions.post("Message", deviceId=device_id, command=play_command)
        print(f"Attempting to play The Office S01E01 on device: {device['Name']}")
else:
    print("The first episode of The Office not found in the library.")
