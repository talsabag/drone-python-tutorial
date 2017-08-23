import requests
import os
import nose
import uuid
import json
import unittest

class UserApiIntegrationTest(unittest.TestCase):

    def setUp(self):
        assert "SERVER_URL" in os.environ
        self._base_url = os.environ['SERVER_URL']
        # Trim the trailing slash
        if self._base_url.endswith('/'):
            self._base_url = self._base_url[:-1]

        self._base_headers = {'Content-Type':'application/json'}
        self.__user = uuid.uuid4()

    def tearDown(self):
        pass

    def test_registration(self):
        url = self._base_url + '/api/v1/user'
        data = '{"email": "%s@email.com", "password": "mypassword"}' % (uuid.uuid4())
        response = requests.post(url, headers=self._base_headers, data=data)
        response.raise_for_status()
        data = json.loads(response.content)

        assert data['id'] != 0
        assert len(data['token']) > 10
        self.__id = data['id']
        self.__token = data['token']

# Should do All but this is just a demo....
