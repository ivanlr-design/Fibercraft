import requests
import hashlib
import json

def request_api(url, api_key, command, args, map=None):
    if map:
        hash_input = f'{command}{args}{map}{api_key}'.encode('utf-8')
    else:
        hash_input = f'{command}{args}{api_key}'.encode('utf-8')
    
    hash_value = hashlib.sha1(hash_input).hexdigest()

    payload = f'command={command}&args={args}&hash={hash_value}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=payload, headers=headers)

    return response.text