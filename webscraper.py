

from requests import get

def get_request():
    request_url = ""
    response = get(request_url)
    print(response.text[:])


