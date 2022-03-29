# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# pip install flask flask-restful
from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import urllib.parse  # needed to decode URL passed from the extension
import feauture_extraction as fe

from colorama import Fore, Style  # fancy colours in terminal

MODEL_HOST = '212.71.244.118'
#HOST = '127.0.0.1'
PORT = '8501'
MODEL_NAME = 'phishingModelAllUrlFeautures'
API_ENDPOINT = 'http://' + MODEL_HOST + ':' + PORT + \
    '/v1/models/' + MODEL_NAME + ':predict'
MAX_ML_OUTPUT = 0.95

# "fake" phishing website used for presentation / testing
HARDCODED_PHISHING = "notreal.test" 

app = Flask(__name__)
api = Api(app)

class Check(Resource):
    """
    Flask needs to know that this class is an endpoint for the API
    thus Resource must be passed in with the class definition
    """
    def post(self):
        """
        Parse the URL received from frontend
        and pass it to other method to check for phishing
        """
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        encodedUrl = args['url']
        url = urllib.parse.unquote(encodedUrl)
        print("url is: " + url)

        # The front-end will block site if response is "true"
        answer = "false"
        if (is_phishing(url)):
            answer = "true"
        return {'answer': answer}, 200


def is_phishing(url):
    """
    Checks URL with the hardcoded phishing.
    Even though the Hardcoded phishing is always
    returning True, the request is sant anyway for
    purpose of the presentation.
    """
    output = send_API_request(url)
    if HARDCODED_PHISHING in url:
        return True
    if output >= MAX_ML_OUTPUT:
        return True
    return False



def send_API_request(url):
    """
    Processes the URL by passing it to UrlFeautures Class
    Then formats the feautures in the way the Model can accept
    Finally, the response from the model is returned from the function.
    """
    print('--------------------------------------------------------------------------------')
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
    return output


api.add_resource(Check, '/check')  # '/check' is entry point of the API

if (__name__ == '__main__'):
    app.run()
