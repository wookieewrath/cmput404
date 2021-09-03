import requests

response = requests.get('https://raw.githubusercontent.com/wookieewrath/cmput404/master/lab1.py')
print(response.content)