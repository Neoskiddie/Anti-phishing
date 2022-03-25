# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# pip install flask flask-restful
from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import urllib.parse  # needed to decode URL passed from the extension
import feauture_extraction as fe

from colorama import Fore, Style  # fancy colours in terminal

HOST = '212.71.244.118'
#HOST = '127.0.0.1'
PORT = '8501'
MODEL_NAME = 'phishingModelAllUrlFeautures'
API_ENDPOINT = 'http://' + HOST + ':' + PORT + \
    '/v1/models/' + MODEL_NAME + ':predict'

app = Flask(__name__)
api = Api(app)


class Check(Resource):  # Flask needs to know that this class is an endpoint for our API, and so we pass Resource in with the class definition
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        encodedUrl = args['url']
        url = urllib.parse.unquote(encodedUrl)
        #print("url is: " + url)
        # Hardcoded "phishing" site is notreal.test
        # The front-end will block site if response is "true"
        answer = "false"
        if (isPhishing(url)):
            answer = "true"
        return {'answer': answer}, 200


def isPhishing(url):
    sendAPIRequest(url)
    if "notreal.test" in url:
        return True


def sendAPIRequest(url):
    print('--------------------------------------------------------------------------------')
    # first one is not phishing, second one is phishing
    print(Fore.GREEN + 'The visited url is: ' + Style.RESET_ALL + url)
    urlFeautures = fe.UrlFeautures(url)
    urlFeauturesList = urlFeautures.get_feautures_list()
    urlFeauturesNamesList = urlFeautures.get_feautures_names()

    data = {}
    for i in range(len(urlFeauturesList)):
        # this needs to be a element in a list
        data[urlFeauturesNamesList[i]] = [[urlFeauturesList[i]]]

    json = {"inputs": data}

    print(Fore.GREEN + 'The JSON data send to server: ' +
          Style.RESET_ALL + str(json))
    response = requests.post(url=API_ENDPOINT, json=json)
    jsonOutput = response.json()
    #print('Server JSON response: ' + str(jsonOutput))
    output = jsonOutput['outputs'][0][0]
    print(Fore.GREEN + 'Reponse from the ML model - chances the website is phishing: ' + Fore.RED +
          str(output) + Style.RESET_ALL)
    print('--------------------------------------------------------------------------------')
    # print(type(output))


api.add_resource(Check, '/check')  # '/check' is entry point of the API

if (__name__ == '__main__'):
    app.run()
