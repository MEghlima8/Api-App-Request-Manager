import requests
import json
from App import config

username = config.configs['API_USERNAME']
password = config.configs['API_PASSWORD']


class Api:
        
    def __init__(self):
        self.target_api_url = config.configs["TARGET_API_URL"]
        self.dom_address = config.configs['DOMAIN_ADDRESS']
        self.headers = { 'Content-Type': 'application/json','Authorization': ''}

    def get_new_access_token(self):
        url = self.target_api_url + '/signin'
        payload = json.dumps({
            "username": username,
            "password": password
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.headers['Authorization'] = json.loads(response.text)['result']['token']
        
        
    def get_res_from_api(self, queue, processing):
        dict = {}
        url = self.target_api_url + '/get-result'
        
        # Get the results of the requests that were in the queue
        for i in queue:
            payload = json.dumps({
                "request_id": i[3]
                })
            if self.headers['Authorization'] == '':
                self.get_new_access_token()   
                
            response = requests.request("POST", url, headers=self.headers, data=payload)
            if json.loads(response.text)['status-code'] == 200:
                status = 'done'
            else:
                status = 'processing'
            if json.loads(response.text)['result'] != i[1]:
                dict[str(i[0])] = [ json.dumps({"result" : json.loads(response.text)['result']}) , status ]

        # Get the results of the requests that were processing
        for i in processing:
            payload = json.dumps({
                "request_id": i[3]
                })
            if self.headers['Authorization'] == '':
                self.get_new_access_token()
                
            response = requests.request("POST", url, headers=self.headers, data=payload)
            if json.loads(response.text)['result'] != i[1]:
                dict[str(i[0])] = [ json.dumps({"result" : json.loads(response.text)['result']}) , 'done' ]
        
        return dict
    

    def add_two_numbers(self,num1,num2):
        target_api_url = self.target_api_url + '/add-two-numbers'
        payload = json.dumps({
        "params": {
            "num1": num1,
            "num2": num2
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        return json.loads(response.text)
    

    def hide_text_in_image(self, text, url):
        target_api_url = self.target_api_url + '/hide-text-in-image'
        payload = json.dumps({
        "params": {
            "url": f'{self.dom_address}{url}',
            "text": text
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        return json.loads(response.text)
      
      
    def hide_text_in_sound(self, text, url):
        target_api_url = self.target_api_url + '/hide-text-in-sound'
        payload = json.dumps({
        "params": {
            "url": f'{self.dom_address}{url}',
            "text": text
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_hidden_text_from_sound(self, url):
        target_api_url = self.target_api_url + '/get-hidden-text-from-sound'
        payload = json.dumps({
        "params": {
            "url": f'{self.dom_address}{url}'
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_hidden_text_from_image(self, url):
        target_api_url = self.target_api_url + '/get-hidden-text-from-image'
        payload = json.dumps({
        "params": {
            "url": f'{self.dom_address}{url}'
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        return json.loads(response.text)        


api = Api()






