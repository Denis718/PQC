from jwt import jwt

def main():
    
    algorithm = 'Dilithium3'

    # payload = None # json empty (payload = {})
    payload = {'iss': 'iss01', 'exp': '1713552059'}
    
    token = jwt.generate_token(algorithm, payload)

    print(f'token jwt: {token}')

    is_valid = jwt.verify_token(algorithm, token)

    print("Valid signature?", is_valid)

if __name__ == '__main__':
    main()