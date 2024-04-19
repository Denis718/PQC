import os
import json
import base64
import oqs

def is_json(json: dict):
  try:
    json.loads(json)
  except ValueError as e:
    return False
  return True

def is_alg_valid(algorithm: str):
  if algorithm in oqs.get_enabled_sig_mechanisms():
    return True
  raise ValueError("Invalid algorithm") 
    
def json_to_base64(json: dict):
  return base64.b64encode(json.encode())

def bytes_to_base64(b: bytes):
  return base64.b64encode(b)

def base64_to_bytes(b: bytes):
  return base64.b64decode(b)

def save_key(filename: str, filebytes: bytes):
  with open(f'{_current_dir()}/{filename}', 'wb') as file: 
    file.write(filebytes)

def read_key(filename: str):
  if os.path.exists(f'{_current_dir()}/{filename}'):
    with open(f'{_current_dir()}/{filename}', 'rb') as file: 
      r = file.read()
    return r
  return None #TODO exection - file not found

def _current_dir():
  return os.path.dirname(os.path.realpath(__file__))