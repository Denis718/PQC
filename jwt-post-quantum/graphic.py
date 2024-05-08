import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import oqs

levels = {1: [], 2: [], 3: [], 4: [], 5: []}

algorithm = ('Dilithium', 'ML-DSA', 'Falcon', 'SPHINCS+-SHA2', 'SPHINCS+-SHAKE')

# def count_level():
#     count = 0
#     for level in levels:
#         if levels[level]:
#             count+=1
#     return count

# def what_is_the_level(mechanism):

#     for level in levels:
#         for sig in levels[level]:
#             if sig == mechanism:
#                 return int(sig[-1])

def main():

    # print(oqs.get_enabled_sig_mechanisms())
    # print(oqs.get_supported_sig_mechanisms())
    
    for mechanism in oqs.get_enabled_sig_mechanisms():
        with oqs.Signature(mechanism) as signature:

            level = signature.details['claimed_nist_level']
             
            if level == 1:
               levels[1].append(mechanism)
            elif level == 2:
                levels[2].append(mechanism)
            elif level == 3:
                levels[3].append(mechanism)
            elif level == 4:
                levels[4].append(mechanism)
            elif level == 5:
                levels[5].append(mechanism)
        

    # print(levels)

    df = pd.read_csv('sig_mechanism_times.csv')
    
    df_all = pd.DataFrame()

    df_all['mean_generate_token'] = pd.Series(df.groupby('sig_mechanism').mean()['generate_token'])
    df_all['std_generate_token'] = pd.Series(df.groupby('sig_mechanism').std()['generate_token'])
    
    df_all['mean_verify_token'] = pd.Series(df.groupby('sig_mechanism').mean()['verify_token'])
    df_all['std_verify_token'] = pd.Series(df.groupby('sig_mechanism').std()['verify_token'])
    
    df_all['size_token'] = pd.Series(df.groupby('sig_mechanism').mean()['size_token'])

    max_x = pd.Series(df.groupby('sig_mechanism').max()['size_token'])
    
    # print(df_all.all)


    graphics = []
    
    for level in levels:
        if levels[level]:
            graphics.append({'level': level, 'mechanisms': levels[level]})

    # print(graphics)


    width = 0.5

    # times graphic
    fig_times = plt.figure(figsize=(16,9))

    ax = fig_times.subplots(len(graphics)) 

    ax_index = 0
    for graphic in graphics:
        level = graphic['level']
        for mechanism in graphic['mechanisms']:
            
            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['mean_generate_token'],
                width,                    
                xerr=df_all.loc[[mechanism]]['std_generate_token'],
                label='generate token',
                color='tab:blue'
            )
            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['mean_verify_token'],
                width,
                xerr=df_all.loc[[mechanism]]['std_verify_token'],
                label='verify token',
                color='tab:orange'
            )
        
        ax[ax_index].set_xscale('log')
        ax[ax_index].set_xlim(0.0001, 1)
        ax[ax_index].set_title(f'NIST Level {level}')

        ax_index+=1

    
    line, label = ax[0].get_legend_handles_labels()         
    fig_times.legend(line[0:2], label, loc='upper right') 
    

    ax[ax_index-1].set_xlabel('time (seconds)', ha='center', size='large')
    fig_times.supylabel('mechanisms')

    plt.tight_layout()
    plt.show()


    # size graphic
    fig_size = plt.figure(figsize=(16,9))

    ax = fig_size.subplots(len(graphics)) 

    ax_index = 0
    for graphic in graphics:
        level = graphic['level']
        for mechanism in graphic['mechanisms']:

            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['size_token'],
                width,                    
                color='tab:green'
            )

        ax[ax_index].set_title(f'NIST Level {level}')
        ax[ax_index].set_xlim(0, (max_x.max() // 10000) * 10000 + 10000)
        ax_index+=1

    ax[ax_index-1].set_xlabel('size (bytes)', x=0.5, y=0.1, ha='center', size='large')
    fig_size.supylabel('mechanisms')
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()