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


def by_level(graphics, id_level, width):    

    fig = plt.figure(figsize=(16,9))

    ax = fig.subplots(2) 

    for graphic in graphics:
        level = graphic['level']
        if level == id_level:
            print(level)
            for mechanism in graphic['mechanisms']:
                ax[0].barh(
                mechanism,
                df_all.loc[[mechanism]]['mean_generate_token'],
                width,                    
                xerr=df_all.loc[[mechanism]]['std_generate_token'],
                label='Geração',
                color='tab:blue'
                )
                ax[0].barh(
                    mechanism,
                    df_all.loc[[mechanism]]['mean_verify_token'],
                    width,
                    xerr=df_all.loc[[mechanism]]['std_verify_token'],
                    label='Verificação',
                    color='tab:orange'
                )

    ax[0].set_xscale('log')
    ax[0].set_xlim(0.0001, 1)
    ax[0].set_title('Tempos de geração e verificação do JWT pós-quântico', size='xx-large')

    ax[0].set_xlabel('Segundos', x=0.5, y=0.1, ha='center', size='xx-large')
   

    line, label = ax[0].get_legend_handles_labels()         
    fig.legend(line[0:2], label, loc='upper right', fontsize='x-large') 
    # fig_size.supylabel('mechanisms')
    ax[0].tick_params(axis="x", labelsize='xx-large')
    ax[0].tick_params(axis="y", labelsize='xx-large')
    
    # plt.tight_layout()
    # plt.savefig("times-jwt.svg")
    # plt.savefig("times-jwt.png")
    # plt.show()


    for graphic in graphics:
        level = graphic['level']
        if level == id_level:
            print(level)
            for mechanism in graphic['mechanisms']:
                ax[1].barh(
                mechanism,
                df_all.loc[[mechanism]]['size_token'],
                width,                    
                color='tab:green'
            )

    ax[1].set_xlabel('Bytes', x=0.5, y=0.1, ha='center', size='xx-large')
    # ax.set_xscale('log')
    # ax.set_xlim(0.0001, 1)
    ax[1].set_title('Tamanho do JWT pós-quântico', size='xx-large')

    ax[1].tick_params(axis="x", labelsize='xx-large')
    ax[1].tick_params(axis="y", labelsize='xx-large')

    fig.supylabel('Mecanismos de assinatura digital', size='xx-large')

    plt.tight_layout()
    # plt.savefig("-jwt.svg")
    # plt.savefig("times-jwt.png")
    plt.show()



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
    # fig_times = plt.figure(figsize=(16,16))

    fig_times, ax = plt.subplots(len(graphics), 1, figsize=(20,12), gridspec_kw={'height_ratios': [3.5, 1.8, 4, 5]}, layout='constrained') 

    ax_index = 0
    for graphic in graphics:
        level = graphic['level']
        for mechanism in graphic['mechanisms']:
            
            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['mean_generate_token'],
                width,                    
                xerr=df_all.loc[[mechanism]]['std_generate_token'],
                label='Geração',
                color='tab:blue',
                error_kw = {'capsize': 3}
            )
            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['mean_verify_token'],
                width,
                xerr=df_all.loc[[mechanism]]['std_verify_token'],
                label='Verificação',
                color='tab:orange',
                error_kw = {'capsize': 3, 'ecolor': 'k'}
            )
        
        ax[ax_index].set_xscale('log')
        ax[ax_index].set_xlim(0.00001, 1)
        ax[ax_index].set_title(f'NIST Level {level}', size='xx-large')

        

        ax[ax_index].tick_params(axis="x", labelsize='xx-large')
        ax[ax_index].tick_params(axis="y", labelsize='xx-large')

        ax_index+=1

    
    line, label = ax[0].get_legend_handles_labels()         
    fig_times.legend(line[0:2], label, loc='outside upper right', fontsize='x-large', ncols=2) 
    

    ax[ax_index-1].set_xlabel('Segundos', x=0.5, y=0.1, ha='center', size='xx-large')
    # fig_times.supylabel('Mecanismos de assinatura digital', size='x-large')
    
    # plt.tight_layout()
    plt.savefig("times-jwt.svg")
    plt.savefig("times-jwt.png")
    plt.show()

    # size graphic
    # fig_size = plt.figure(figsize=(16,16))

    fig_size, ax = plt.subplots(len(graphics), 1, figsize=(20,12), gridspec_kw={'height_ratios': [3.5, 1.8, 4, 5]}, layout='constrained')

    ax_index = 0
    for graphic in graphics:
        level = graphic['level']
        for mechanism in graphic['mechanisms']:

            ax[ax_index].barh(
                mechanism,
                df_all.loc[[mechanism]]['size_token'],
                width,                    
                color='tab:green',
            )

        ax[ax_index].set_title(f'NIST Level {level}', size='xx-large')
        ax[ax_index].set_xlim(0, (max_x.max() // 10000) * 10000 + 10000)

        ax[ax_index].tick_params(axis="x", labelsize='xx-large')
        ax[ax_index].tick_params(axis="y", labelsize='xx-large')
        
        ax_index+=1

    ax[ax_index-1].set_xlabel('Bytes', x=0.5, y=0.1, ha='center', size='xx-large')
    

    # fig_size.supylabel('Mecanismos de assinatura digital', size='xx-large')
    
    # plt.tight_layout()
    plt.savefig("sizes-jwt.svg")
    plt.savefig("sizes-jwt.png")
    plt.show()

if __name__ == '__main__':
    main()