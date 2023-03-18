import json
import base64

from Crypto.Cipher import AES


def rawToJson(raw_prop: str):
    result = {}
    for prop in raw_prop.split('&'):
        (key, value) = prop.split('=')
        result.update({key: value})
    json_prop = json.dumps(result)
    return json_prop

def dictToRaw(dict_prop: dict):
    list_prop = []
    for key in dict_prop:
        list_prop.append('{}={}'.format(key, dict_prop[key]))
    return "&".join(list_prop)
    

def generateToken(prop: dict):
    key = b'webapp1.0+202106'
    raw_prop = dictToRaw(prop).encode()
    prop_padded = raw_prop + (AES.block_size - (len(raw_prop) % AES.block_size)) * b'\x00'
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    return base64.b64encode(cipher.encrypt(prop_padded))
