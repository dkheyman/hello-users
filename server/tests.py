import requests
import os
import time

fqdn = os.environ.get('FQDN', 'http://localhost')
if fqdn == 'http://localhost':
    port = os.environ.get('PORT', '5000')
    url = fqdn + ":" + str(port) + "/hello"
else:
    url = fqdn + "/dev/hello"

headers = {
    'Content-Type': 'application/json'
}

def test_put():
    data = {
        "dateOfBirth": "2000-12-12"
    }

    response = requests.put(url+"/testuser", json=data, headers=headers)
    return response.status_code == 200
    
def test_get():
    response = requests.get(url+"/testuser", headers=headers)
    return response.status_code == 200

assert(test_put())
assert(test_get())
