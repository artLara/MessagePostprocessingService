import psutil
import requests
import json

class Utils:
    @staticmethod
    def checkRamSize():
       return psutil.virtual_memory().total/(1024**3) > 18.0
    
    # def sendMessage(message):
    #     data_json = json.dumps(dataDict)
    #     payload = {'json_payload': dataDict}
    #     create_headers = {'Content-Type': 'application/json'}
    #     r = requests.get('http://localhost:8000/classifier/api/v1/', data=json.dumps(payload))
