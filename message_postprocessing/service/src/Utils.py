import psutil
import requests
import json
import editdistance

class Utils:
   def __init__(self):
      pass
    
   @staticmethod
   def checkRamSize():
      return psutil.virtual_memory().total/(1024**3) > 18.0
   
   @staticmethod
   def metricEditDistanceModify(validWord, noiseWord, prob, pond):
      distance = editdistance.eval(validWord, noiseWord)
      distance = min(len(validWord), distance)
      return 1 - distance/len(validWord) + prob * pond
    
    # def sendMessage(message):
    #     data_json = json.dumps(dataDict)
    #     payload = {'json_payload': dataDict}
    #     create_headers = {'Content-Type': 'application/json'}
    #     r = requests.get('http://localhost:8000/classifier/api/v1/', data=json.dumps(payload))
