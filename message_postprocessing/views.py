from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse

from rest_framework.response import Response
import json
import requests
import sys

from message_postprocessing.service.src.PhraseCleaner import PhraseCleaner
sys.path.append('../')
sys.path.append('../../')


phraseCleaner = PhraseCleaner()
message = {'index':1, 'phrase':'This is a test'}

class Post_APIView(APIView):
    

    def get(self, request, format=None, *args, **kwargs):
        data = request.body
        data = json.loads(data)

        # print('------>Data:', data)
        # print('------>Data:', type(data))
        message['phrase'] = phraseCleaner.cleanSentence(jsonData=data)
        message['index'] += 1
        print(message)
        response = {
           "message": "OK",
           "error": False,
           "code": 200,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        
        return JsonResponse(message)
        # return Response(serializer.data)
