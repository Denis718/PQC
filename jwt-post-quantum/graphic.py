import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import oqs
import os

import utils

data_times = [(
    'mean_generate_token',
    'std_generate_token',
    'tab:blue',
    'Generate',
),(
    'mean_verify',
    'std_verify',
    'tab:orange',
    'Verify',
)]

data_sizes = [(
    'mean_size',
    'tab:blue',
    'Size',
)]

def plot_times_by_level(df_all, level, graphics):
    df_all = utils.one_level(df_all, level, graphics)
    plot_times_all(df_all, level)

def plot_sizes_by_level(df_all, level, graphics):
    df_all = utils.one_level(df_all, level, graphics)
    plot_sizes_all(df_all, level)


def plot_times_all(df_all, level):

    y = np.arange(len(df_all.index)-1, -1, -1) 
    width = 0.3

    fig, ax = plt.subplots(figsize=(16,9), layout='constrained') 

    for i, d in enumerate(data_times):
        ax.barh(
            y - i * width, 
            [df_all.iloc[j][d[0]] for j in range(len(df_all.index))],
            width,
            xerr=[df_all.iloc[j][d[1]] for j in range(len(df_all.index))],
            label=d[3],
            color=d[2],
            error_kw = {'capsize': 2, 'ecolor': 'k'}
        )

    ax.set(yticks=y - (len(data_times) - 1) * width / 2, yticklabels=df_all.index.to_list())

    # if level:
    #     ax.set_title(f'NIST Level {level}', size='xx-large')

    ax.set_xlabel('Segundos', x=0.5, y=0.1, ha='center', size='xx-large')
    ax.set_xscale('log')
    ax.set_xlim(0.000001, 1.0)
    ax.set_ylim(-1 + width + (width/2), len(df_all.index)-1 + width)

    ax.tick_params(axis="x", labelsize='xx-large')
    ax.tick_params(axis="y", labelsize='xx-large')
    
    ax.legend()
    
    if level:
        plt.savefig(f'./out/jwt_times_level_{level}.svg')
    else:
        plt.savefig(f'./out/jwt_times_all_level.svg')

    plt.show()

def plot_sizes_all(df_all, level):

    fig, ax = plt.subplots(figsize=(16,9), layout='constrained') 

    y = np.arange(len(df_all.index)-1, -1, -1) 

    width = 0.20

    for i, d in enumerate(data_sizes):
        ax.barh(
            y - i * width,
            [df_all.iloc[j][d[0]] for j in range(len(df_all.index))],
            width,
            label=d[2],
            color=d[1],
        )
    
    ax.set(yticks=y - (len(data_sizes) - 1) * width / 2, yticklabels=df_all.index.to_list())

    # if level:
    #     ax.set_title(f'NIST Level {level}', size='xx-large')

    ax.set_xlabel('Bytes', x=0.5, y=0.1, ha='center', size='xx-large')
    ax.set_xscale('log')
    ax.set_xlim(1, 10000000)
    ax.set_ylim(-1 + (width*2) +width, len(df_all.index)-1 + (width*2))
        
    ax.tick_params(axis="x", labelsize='xx-large')
    ax.tick_params(axis="y", labelsize='xx-large')

    ax.legend()

    if level:
        plt.savefig(f'./out/jwt_sizes_level_{level}.svg')
    else:
        plt.savefig(f'./out/jwt_sizes_all_level.svg')

    plt.show()

def plot_times_split_level(df_all, graphics):

    dfs = []

    dfs.append((utils.one_level(df_all, 1, graphics), '1'))
    dfs.append((utils.one_level(df_all, 2, graphics), '2'))
    dfs.append((utils.one_level(df_all, 3, graphics), '3'))
    dfs.append((utils.one_level(df_all, 4, graphics), '4'))
    dfs.append((utils.one_level(df_all, 5, graphics), '5'))

    fig, ax = plt.subplots(
        len(graphics),
        1,
        sharex=True,
        figsize=(16,9),
        gridspec_kw={'height_ratios': [s for s in [ len(g['mechanisms']) for g in graphics]]},
        layout='constrained'
    ) 

    ax_index = 0
    
    for m in dfs:
        df=m[0]
        l=m[1]
        
        y = np.arange(len(df.index)-1, -1, -1) 
        width = 0.3

        if not df.empty: 
            for i, d in enumerate(data_times):
                ax[ax_index].barh(
                    y - i * width, 
                    [df.iloc[j][d[0]] for j in range(len(df.index))],
                    width,
                    xerr=[df.iloc[j][d[1]] for j in range(len(df.index))],
                    label=d[3],
                    color=d[2],
                    error_kw = {'capsize': 2, 'ecolor': 'k'},
                )

            ax[ax_index].set(yticks=y - (len(data_times) - 1) * width / 2, yticklabels=df.index.to_list())

            ax[ax_index].set_title(f'NIST Level {l}', size='xx-large')

            ax[ax_index].set_xscale('log')
            ax[ax_index].set_xlim(0.000001, 1.0)
            ax[ax_index].set_ylim(-1 + width + (width/2), len(df.index)-1 + width)

            ax[ax_index].tick_params(axis="x",  labelsize='xx-large')
            ax[ax_index].tick_params(axis="y", labelsize='xx-large')

            ax_index+=1
            
    line, label = ax[0].get_legend_handles_labels()         
    legend = fig.legend(line[0:3], label,  fontsize='x-large') 
    legend.get_frame().set(alpha=1.0)

    ax[ax_index-1].set_xlabel('Segundos', x=0.5, y=0.1, ha='center', size='xx-large')

    plt.savefig('./out/jwt_times_split_level.svg')
    plt.show()

def plot_sizes_split_level(df_all, graphics):

    dfs = []

    dfs.append((utils.one_level(df_all, 1, graphics), '1'))
    dfs.append((utils.one_level(df_all, 2, graphics), '2'))
    dfs.append((utils.one_level(df_all, 3, graphics), '3'))
    dfs.append((utils.one_level(df_all, 4, graphics), '4'))
    dfs.append((utils.one_level(df_all, 5, graphics), '5'))

    fig, ax = plt.subplots(
        len(graphics),
        1,
        sharex=True,
        figsize=(16,9),
        gridspec_kw={'height_ratios': [s for s in [ len(g['mechanisms']) for g in graphics]]},
        layout='constrained'
    ) 

    ax_index = 0

    for m in dfs:
        df=m[0]
        l=m[1]
 
        y = np.arange(len(df.index)-1, -1, -1) 
        width = 0.4
        
        if not df.empty: 
            for i, d in enumerate(data_sizes):
                ax[ax_index].barh(
                    y - i * width,
                    [df.iloc[j][d[0]] for j in range(len(df.index))],
                    width,
                    label=d[2],
                    color=d[1],
                )

            ax[ax_index].set(yticks=y - (len(data_sizes) - 1) * width / 2, yticklabels=df.index.to_list())

            ax[ax_index].set_title(f'NIST Level {l}', size='xx-large')

            ax[ax_index].set_xscale('log')
            ax[ax_index].set_xlim(1,10000000)
            ax[ax_index].set_ylim(-1 + width + (width/2), len(df.index)-1 + width)

            ax[ax_index].tick_params(axis="x", labelsize='xx-large')
            ax[ax_index].tick_params(axis="y", labelsize='xx-large')

            ax_index+=1

    ax[ax_index-1].set_xlabel('Bytes', x=0.5, y=0.1, ha='center', size='xx-large')
             
    line, label = ax[0].get_legend_handles_labels()         
    legend = fig.legend(line[0:4], label,  fontsize='x-large') 
    legend.get_frame().set(alpha=1.0)
    
    plt.savefig('./out/jwt_sizes_split_level.svg')
    plt.show()

def main():

    levels = {1: [], 2: [], 3: [], 4: [], 5: []}

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
    
    if not os.path.exists('./out'):
        os.makedirs('./out')
  
    df = pd.read_csv('jwt_times_sizes.csv')
    
    df_all = pd.DataFrame(index=oqs.get_enabled_sig_mechanisms())

    df_all['mean_generate_token'] = pd.Series(df.groupby('sig_mechanism').mean()['generate_token'])
    df_all['std_generate_token'] = pd.Series(df.groupby('sig_mechanism').std()['generate_token'])
    
    df_all['mean_verify'] = pd.Series(df.groupby('sig_mechanism').mean()['verify_token'])
    df_all['std_verify'] = pd.Series(df.groupby('sig_mechanism').std()['verify_token'])

    df_all['mean_size'] = pd.Series(df.groupby('sig_mechanism').mean()['size_token'])
    
    print(df_all)

    graphics = []
    for level in levels:
        if levels[level]:
            graphics.append({'level': level, 'mechanisms': levels[level]})

    plot_times_all(df_all, None)
    plot_times_by_level(df_all, 1, graphics)
    plot_times_by_level(df_all, 2, graphics)
    plot_times_by_level(df_all, 3, graphics)
    plot_times_by_level(df_all, 4, graphics)
    plot_times_by_level(df_all, 5, graphics)

    plot_times_split_level(df_all, graphics)
    
    plot_sizes_all(df_all, None)
    plot_sizes_by_level(df_all, 1, graphics)
    plot_sizes_by_level(df_all, 2, graphics)
    plot_sizes_by_level(df_all, 3, graphics)
    plot_sizes_by_level(df_all, 4, graphics)
    plot_sizes_by_level(df_all, 5, graphics)

    plot_sizes_split_level(df_all, graphics)

if __name__ == '__main__':
    main()