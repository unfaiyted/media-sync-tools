import os
import requests


class Chat:
    def __init__(self, client, account):
        self.client = client
        self.account = account

