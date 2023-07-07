import requests
import unittest
from unittest.mock import MagicMock
import sys
import os

# Add the parent folder to the module search path
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_folder)

from utils.portainer import PortainerClient
class PortainerClientTests(unittest.TestCase):
    def setUp(self):
        self.client = PortainerClient('http://192.168.0.120:9001', 'faiyt', 'PASSWORD')
        self.client._authenticate = MagicMock(return_value='dummy_token')

    def test_get_container_id_found(self):
        container_name = 'plex'
        containers = [
            {'Id': '123', 'Names': ['/plex']},
            {'Id': '456', 'Names': ['/other']},
        ]
        self.client._get_containers = MagicMock(return_value=containers)

        container_id = self.client.get_container_id(container_name)
        self.assertEqual(container_id, '123')

    def test_get_container_id_not_found(self):
        container_name = 'plex'
        containers = [
            {'Id': '456', 'Names': ['/other']},
        ]
        self.client._get_containers = MagicMock(return_value=containers)

        container_id = self.client.get_container_id(container_name)
        self.assertIsNone(container_id)

    def test_restart_container_success(self):
        container_name = 'plex'
        container_id = '123'
        self.client.get_container_id = MagicMock(return_value=container_id)
        self.client._get_headers = MagicMock(return_value={'X-API-Key': 'dummy_token', 'Authorization': 'Bearer dummy_token'})
        requests.post = MagicMock(return_value=MagicMock(status_code=204))

        result = self.client.restart_container(container_name)
        self.assertTrue(result)

    def test_restart_container_failure(self):
        container_name = 'plex'
        container_id = '123'
        self.client.get_container_id = MagicMock(return_value=container_id)
        self.client._get_headers = MagicMock(return_value={'X-API-Key': 'dummy_token', 'Authorization': 'Bearer dummy_token'})
        requests.post = MagicMock(return_value=MagicMock(status_code=500))

        result = self.client.restart_container(container_name)
        self.assertFalse(result)

    # Add similar tests for stop_container() and start_container()

if __name__ == '__main__':
    unittest.main()
