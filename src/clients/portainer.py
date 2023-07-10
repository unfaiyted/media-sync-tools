import requests
import json

class PortainerClient:
    def __init__(self, portainer_url, username, password):
        self.portainer_url = portainer_url
        self.username = username
        self.password = password
        self.jwt_token = self._authenticate()

    def _authenticate(self):
        auth_response = requests.post(f'{self.portainer_url}/api/auth', data=json.dumps({"Username": self.username, "Password": self.password}), headers={'content-type': 'application/json'}).json()
        return auth_response['jwt']

    def _get_headers(self):
        return {
            'X-API-Key': self.jwt_token,
            'Authorization': f'Bearer {self.jwt_token}'
        }

    def _get_containers(self):
        headers = self._get_headers()
        containers_response = requests.get(f'{self.portainer_url}/api/endpoints/2/docker/containers/json?all=true', headers=headers)
        return containers_response.json()

    def get_container_id(self, container_name):
        containers = self._get_containers()
        for container in containers:
            if '/'+container_name in container['Names']:
                return container['Id']
        return None

    def restart_container(self, container_name):
        container_id = self.get_container_id(container_name)
        if container_id is None:
            print(f'No container found with name: {container_name}')
            return False

        headers = self._get_headers()
        restart_response = requests.post(f'{self.portainer_url}/api/endpoints/2/docker/containers/{container_id}/restart', headers=headers)
        if restart_response.status_code == 204:
            print(f'Successfully restarted container: {container_name}')
            return True
        else:
            print(f'Failed to restart container: {container_name}')
            return False

    def stop_container(self, container_name):
        container_id = self.get_container_id(container_name)
        if container_id is None:
            print(f'No container found with name: {container_name}')
            return False

        headers = self._get_headers()
        stop_response = requests.post(f'{self.portainer_url}/api/endpoints/2/docker/containers/{container_id}/stop', headers=headers)
        if stop_response.status_code == 204:
            print(f'Successfully stopped container: {container_name}')
            return True
        else:
            print(f'Failed to stop container: {container_name}')
            return False

    def start_container(self, container_name):
        container_id = self.get_container_id(container_name)
        if container_id is None:
            print(f'No container found with name: {container_name}')
            return False

        headers = self._get_headers()
        start_response = requests.post(f'{self.portainer_url}/api/endpoints/2/docker/containers/{container_id}/start', headers=headers)
        if start_response.status_code == 204:
            print(f'Successfully started container: {container_name}')
            return True
        else:
            print(f'Failed to start container: {container_name}')
            return False
