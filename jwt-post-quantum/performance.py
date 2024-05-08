import pandas as pd
import matplotlib.pyplot as plt
import time
import oqs 
import sys

from jwt import jwt

def main():

    if len(sys.argv) == 2:
        if not sys.argv[1].isdigit(): 
            print(f'Usage: python {sys.argv[0]} <run_numbers>')
            exit()

    list_df = []

    for sig_mechanism in oqs.get_enabled_sig_mechanisms():
        
        generate_token_times = []
        verify_token_times = []
        size_token = []
        
        df = pd.DataFrame({'sig_mechanism': [], 'generate_token': [], 'verify_token': []})

        df['sig_mechanism'] = pd.Series([sig_mechanism] * int(sys.argv[1]))
    
        for i in range(int(sys.argv[1])):

            # print(i, sig_mechanism)
            
            # payload = None # json empty (payload = {})
            payload = {'iss': 'iss01', 'exp': '1713552059'}
            
            start_generate_token = time.time()
            token = jwt.generate_token(sig_mechanism, payload)
            end_generate_token = time.time()

            size_token.append(len(token.encode()))
            
            generate_token_times.append(end_generate_token - start_generate_token)

            start_verify_token = time.time()
            is_valid = jwt.verify_token(sig_mechanism, token)
            end_verify_token = time.time()

            verify_token_times.append(end_verify_token - start_verify_token)

        df['generate_token'] = pd.Series(generate_token_times)
        df['verify_token'] = pd.Series(verify_token_times)
        df['size_token'] = pd.Series(size_token)

       
        list_df.append(df)

    all_df = pd.concat(list_df)

    all_df = all_df.set_index('sig_mechanism')

    print(all_df)
    
    all_df.to_csv('sig_mechanism_times.csv', index=True)

    print('File sig_mechanism_times.csv was created')

if __name__ == '__main__':
    main()