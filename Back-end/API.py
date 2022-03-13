# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# pip install flask flask-restful
from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import urllib.parse  # needed to decode URL passed from the extension
import feauture_extraction as fe

HOST = '212.71.244.118'
#HOST = '127.0.0.1'
PORT = '8501'
MODEL_NAME = 'phishingModel'
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
        print("url is: " + url)
        # Hardcoded "phishing" site is notreal.test
        # The front-end will block site if response is "true"
        answer = "false"
        if (isPhishing(url)):
            answer = "true"
        return {'answer': answer}, 200


def isPhishing(url):
    sendAPIRequest(url)
    if "notreal.text" in url:
        return True


def sendAPIRequest(url):
    # first one is not phishing, second one is phishing
    print("The visited url is: " + url)
    urlFeautures = fe.UrlFeautures(url)
    urlFeauturesList = urlFeautures.get_feautures_list()
    urlFeauturesNamesList = urlFeautures.get_feautures_names()

    data = {}
    for i in range(len(urlFeauturesList)):
        # this needs to be a element in a list
        data[urlFeauturesNamesList[i]] = [[urlFeauturesList[i]]]

    json = {"inputs": data}

    print(json)
    response = requests.post(url=API_ENDPOINT, json=json)
    jsonOutput = response.json()
    output = jsonOutput['outputs'][0][0]
    print(output)
    print(type(output))


api.add_resource(Check, '/check')  # '/check' is entry point of the API

if (__name__ == '__main__'):
    app.run()
