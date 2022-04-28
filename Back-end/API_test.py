"""
Simple script to test single phishing URL against the API.
"""
import requests
import urllib.parse

url = 'https://gbronka.com:2096/check'
url_to_check = urllib.parse.quote(input('Enter URL:').strip())
myobj = {'url': url_to_check}

x = requests.post(url, json = myobj)

answer = x.json()['answer']
print('The website is phishing: ' + answer)
