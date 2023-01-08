"""
Script testing the list of URLs in test_URLs.txt file
"""
import requests
import urllib.parse

my_file = open('./Data/test_URLs.txt', 'r')

url = 'https://gbronka.com:2096/check'

list_of_answers = []
for line in my_file:
    url_to_check = urllib.parse.quote(line)
    myobj = {'url': url_to_check}
    x = requests.post(url, json=myobj)
    answer = x.json()['answer']
    list_of_answers.append(answer)

print(list_of_answers)
