# Plex Emby Sync Tools
nlex Emby Sync Tools is a Python project that provides tools for synchronizing content between Plex and Emby media servers.

### Requirements
Python 3.x
FastAPI
Starlette
### Installation
To install Plex Emby Sync Tools, follow these steps:

1. Clone the repository:
    `git clone https://github.com/your-username/plex-emby-sync-tools.git`
2. Change into the project directory:
`cd plex-emby-sync-tools`
3. Install the required dependencies:
`pip install -r requirements.txt`

### Usage
To run the Plex Emby Sync Tools server, execute the following command:

`python main.py`
The server will start and listen on http://localhost:8000/ by default.

### Endpoints
The Plex Emby Sync Tools server provides the following endpoints:

`/sync/watchlist`: Trigger the synchronization of the watchlist.
`/sync/collection`: Trigger the synchronization of collections.
`/examples`: Trigger example operations for testing purposes.
`/webhook`: Handle incoming webhooks from external services.
`/recommendations`: Retrieve AI-based content recommendations.
`/sync/trakt`: Perform synchronization with Trakt, if integrated.
`/sync/config`: Retrieve information about the current configuration.
`/healthcheck`: Check the health status of the server.
`/get/command`: Retrieve voice commands, if applicable.

#### Webhook
Plex Emby Sync Tools supports webhooks to receive and process data from external services. To integrate with webhooks, send POST requests to the /webhook endpoint with appropriate data in the request body.

#### Recommendations
The project includes functionality to generate content recommendations based on various criteria. To trigger the recommendation process, send a GET request to the /recommendations endpoint.

#### Trakt Integration
WIP: Plex Emby Sync Tools can be integrated with Trakt for seamless content synchronization. To utilize Trakt integration, configure the appropriate settings and trigger synchronization via the /sync/trakt endpoint.

#### Configuration
The project's configuration can be managed via the config module. Details about various settings and options can be found in the configuration file.

#### Health Check
The /healthcheck endpoint is available to ensure the server's health. Accessing this endpoint will return a message indicating the server's status.

#### Voice Command
WIP: If your project includes voice command functionality, users can interact with the system using voice commands. The /get/command endpoint provides access to available voice commands.

#### Contributing
We welcome contributions from the community! If you want to contribute to Plex Emby Sync Tools, please follow the guidelines outlined in CONTRIBUTING.md.

#### License
Plex Emby Sync Tools is licensed under the MIT License.
