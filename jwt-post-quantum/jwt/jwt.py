import oqs
import json
from pprint import pprint

# internal import
from . import utils

def _generate_header(algorithm: str):
    try:       
        if utils.is_alg_valid(algorithm):
            header = {'alg': algorithm, 'typ': 'JWT'}
            return json.dumps(header)
    except ValueError as e:
        print(f'{e}: Choose between one of the valid algorithms\n{oqs.get_enabled_sig_mechanisms()}')
        exit()

# data = header + payload
def _generate_data(algorithm: str, payload: dict =None):

    header_json = _generate_header(algorithm)

    if payload:
        payload_json = json.dumps(payload)
    else:
        payload_json = json.dumps({})

    pprint(f'header json: {header_json}')
    pprint(f'payload json: {payload_json}')

    header_base64_str = utils.json_to_base64(header_json).decode()
    payload_base64_str = utils.json_to_base64(payload_json).decode()

    return f'{header_base64_str}.{payload_base64_str}'

def _split_token(token: str):
    
    x = token.split('.')

    if len(x) > 3:
        # TODO exception
        print('More than three parts')
        exit()

    # header, payload, signature
    return x[0], x[1], x[2]

def _join_data(header_base64_str: str, payload_base64_str: str):
    return f'{header_base64_str}.{payload_base64_str}'

def _sign(algorithm: str, data_base64_str: str):

    with oqs.Signature(algorithm) as signer:
        pprint(signer.details)
        public_key = signer.generate_keypair()
        private_key = signer.export_secret_key()
        signature = signer.sign(data_base64_str.encode())
        
    utils.save_key('public.key', public_key)
    utils.save_key('private.key', private_key)
    
    return signature

def _verify(algorithm: str, data_bytes: bytes, signature_bytes: bytes):

    public_key = utils.read_key('public.key')
    private_key = utils.read_key('private.key')

    with oqs.Signature(algorithm, private_key) as verifier:
        is_valid = verifier.verify(data_bytes, signature_bytes, public_key)

    return is_valid

def generate_token(algorithm: str, payload: dict):

    data_base64_str = _generate_data(algorithm=algorithm, payload=payload)

    print(f'data base64: {data_base64_str}')

    signature = _sign(algorithm, data_base64_str)
    
    signature_base64_str = utils.bytes_to_base64(signature).decode()

    return f'{data_base64_str}.{signature_base64_str}'

def verify_token(algorithm: str, token: str):

    header, payload, signature = _split_token(token)

    data_bytes = _join_data(header, payload).encode()

    signature_bytes = utils.base64_to_bytes(signature)

    return _verify(algorithm, data_bytes, signature_bytes)

   
