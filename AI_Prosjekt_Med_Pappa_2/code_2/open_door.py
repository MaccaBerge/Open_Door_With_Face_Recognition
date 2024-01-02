import requests
import time


class Open_Door:
    def __init__(self, request_delay: int | float = 11.0):
        self.url = 'https://10.0.0.180:1880/endpoint/test'
        self.body_content = b'test'
        self.request_delay = request_delay
        self.last_request_time = 0
        self.request_delay = 0 # for test only
        
    def send_open_door_request(self):
        self.current_request_time = time.time()
        time_since_last_request = self.current_request_time - self.last_request_time

        if time_since_last_request > self.request_delay:
            response = requests.post(self.url, self.body_content, verify=False)
            print(f'Status Code: {response.status_code}')
            print(f'Response Content: {response.content}')

            self.last_request_time = self.current_request_time

