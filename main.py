import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from f1data import getdata
import sys
import os

args = sys.argv
try:
    args = args[1]
except:
    exit('Please provide arguments: main.py upa ( to *u*pdate & *p*lot and *a*nalyze the data or only one to do that specific task)')
    
# check if data is already in data folder else create it
path = os.getcwd() + r'\data'
plotpath = os.getcwd() + r'\plots'
circuitpath = os.getcwd() + r'\plots\circuits'

custom_colors = [   '#945417', '#1eabfa', '#a22780', '#ecb920',
                    '#7f6e34', '#1e3d59', '#c5521b', '#800e34',
                    '#00bb6c', '#e28fc3', '#704b5b', '#e39e83',
                    '#baccc6', '#77ad95', '#eee9db', '#ee4769']

licircuits =    ['Austrian Grand Prix', 'Belgian Grand Prix', 'British Grand Prix',
                'Canadian Grand Prix', 'Italian Grand Prix', 'Monaco Grand Prix']
            
ligroups =      ['Engine', 'Gearbox', 'Powertrain', 'Suspension', 'Electrical', 'Tyre',
                 'Fluid systems', 'Chassis', 'Driver-related', 'Overheating', 'Accident',
                 'Not classified', 'Disqualified', 'Turbo']

# check if args contains u 
if not os.path.exists(os.path.join(path,r'turbo_era.csv')) or 'u' in args:
    print('Getting data...')
    getdata(1977, 1989).to_csv(os.path.join(path,r'turbo_era.csv'), index=False)
    getdata(2014, 2024).to_csv(os.path.join(path,r'hybrid_era.csv'), index=False)
    print('Data saved to data folder')

# check if args contains p
if 'p' in args:
    print('Plotting data...')
    for file in os.listdir(path):
        if file.endswith('.csv'):
            df_data = pd.read_csv(os.path.join(path,file))
            df_data = df_data[df_data['status'] != 'Finished']
            df_data = df_data[df_data['status'] != 'Not classified']
            
            # group data by date and status
            df_data_ds = df_data.groupby(['year', 'status']).size().reset_index(name='counts')
            
            # pivot data
            df_data_ds = df_data_ds.pivot(index='year', columns='status', values='counts')
            
            # plot data
            df_data_ds.plot(kind='bar', stacked=True, figsize=(15, 5), color=custom_colors)
            if file == 'turbo_era.csv':
                plt.title('F1 Breakdowns (1977 - 1988)')
                plt.ylim(0, 300)
                plt.yticks(range(0, 300, 25))
            else:
                plt.title('F1 Breakdowns (2014 - 2023)')
                plt.ylim(0, 150)
                plt.yticks(range(0, 150, 25))

            plt.xlabel('Year')
            plt.ylabel('Amount')
            plt.legend(bbox_to_anchor=(0.9999, 1))
            plt.savefig(os.path.join(plotpath, file[:-4] + '.png'))
            plt.clf()

            # group data by circuit and status and year
            df_data_ds = df_data.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
            
            
            # filter data for only circuits in the list
            df_data_ds = df_data_ds[df_data_ds['circuit'].isin(licircuits)]

            # pivot data for each circuit
            for circuit in df_data_ds['circuit'].unique():
                df_data_ds_circuit = df_data_ds[df_data_ds['circuit'] == circuit]
                df_data_ds_circuit = df_data_ds_circuit.pivot(index='year', columns='status', values='counts')
                
                # plot data
                df_data_ds_circuit.plot(kind='bar', stacked=True, figsize=(15, 5), color=custom_colors)
                plt.title('F1 Breakdowns (' + str(circuit) + ')')
                plt.xlabel('Year')
                plt.ylabel('Amount')
                plt.ylim(0, 25)
                plt.yticks(range(0, 25, 5))
                plt.legend(bbox_to_anchor=(0.9999, 1))
                plt.savefig(os.path.join(circuitpath, file[:-4] + '_' + str(circuit) + '.png'))
                plt.clf()
                
    print('Plots saved to plots folder')

if 'a' in args:
    print('Analyzing data...')
    # check if data is already in data folder else exit
    if not os.path.exists(os.path.join(path,r'turbo_era.csv')) or not os.path.exists(os.path.join(path,r'hybrid_era.csv')):
        exit('Data not found, please run main.py with the u argument first')

    # get both datasets
    df_turbo = pd.read_csv(os.path.join(path,r'turbo_era.csv'))
    df_hybrid = pd.read_csv(os.path.join(path,r'hybrid_era.csv'))
    
    # drop the finished status rows
    df_turbo = df_turbo[df_turbo['status'] != 'Finished']
    df_hybrid = df_hybrid[df_hybrid['status'] != 'Finished']
    df_turbo = df_turbo[df_turbo['status'] != 'Not classified']
    df_hybrid = df_hybrid[df_hybrid['status'] != 'Not classified']
    
    # transform data to have the groups as rows and the years as columns
    df_turbo_ys = df_turbo.groupby(['year', 'status']).size().reset_index(name='counts')
    df_turbo_ys = df_turbo_ys.pivot(index=['status'], columns='year', values='counts')
    df_turbo_ys = df_turbo_ys.fillna(0)
    
    df_hybrid_ys = df_hybrid.groupby(['year', 'status']).size().reset_index(name='counts')
    df_hybrid_ys = df_hybrid_ys.pivot(index=['status'], columns='year', values='counts')
    df_hybrid_ys = df_hybrid_ys.fillna(0)
    
    # correlation between the status
    plt.title('Year Correlation Turbo era')
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    heatmap = sns.heatmap(df_turbo_ys.corr(), annot=True, cmap="Blues", fmt='.2g')
    plt.savefig(os.path.join(plotpath, 'year_correlation_turbo.png'))
    plt.clf()
    
    plt.title('Year Correlation Hybrid era')
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    heatmap = sns.heatmap(df_hybrid_ys.corr(), annot=True, cmap="Greens", fmt='.2g')
    plt.savefig(os.path.join(plotpath, 'year_correlation_hybrid.png'))
    plt.clf()
    
    #replace the each year in the year column with a number
    df_turbo['year'] = df_turbo['year'].replace({1977: 1, 1978: 2, 1979: 3, 1980: 4, 1981: 5, 1982: 6, 1983: 7, 1984: 8, 1985: 9, 1986: 10, 1987: 11, 1988: 12})
    df_hybrid['year'] = df_hybrid['year'].replace({2014: 1, 2015: 2, 2016: 3, 2017: 4, 2018: 5, 2019: 6, 2020: 7, 2021: 8, 2022: 9, 2023: 10})
    
    df_turbo_newys = df_turbo.groupby(['year', 'status']).size().reset_index(name='counts')
    df_turbo_newys = df_turbo_newys.pivot(index=['status'], columns='year', values='counts')
    
    df_hybrid_newys = df_hybrid.groupby(['year', 'status']).size().reset_index(name='counts')
    df_hybrid_newys = df_hybrid_newys.pivot(index=['status'], columns='year', values='counts')

    # reindex the dataframes with the ligroups
    df_turbo_newys = df_turbo_newys.reindex(ligroups, level=0, fill_value=0)
    df_hybrid_newys = df_hybrid_newys.reindex(ligroups, level=0, fill_value=0)
    
    # Sort the rows by the index
    df_turbo_newys.sort_index(inplace=True)
    df_hybrid_newys.sort_index(inplace=True)
    
    # plot the correlation between the two eras as a line chart with data points
    plt.title('Correlation between Turbo and Hybrid era')
    plt.ylabel('Correlation')
    plt.xlabel('Compared Years')
    plt.xticks(np.arange(1, 11, 1), [str(x) + '-' + str(x + 37) for x in range(1977, 1987)])
    plt.yticks(np.arange(-1.1, 1.1, 0.1))
    plt.ylim(-1, 1)
    plt.plot(df_turbo_newys.corrwith(df_hybrid_newys), marker='o')
    plt.savefig(os.path.join(plotpath, 'correlation_turbo_hybrid.png'))
    plt.clf()
    
    # filter data for only circuits in the list
    df_turbo = df_turbo[df_turbo['circuit'].isin(licircuits)]
    df_hybrid = df_hybrid[df_hybrid['circuit'].isin(licircuits)]

    df_turbo_circuit = df_turbo.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
    df_turbo_circuit = df_turbo_circuit.pivot(index=['circuit', 'status'], columns='year', values='counts')
    df_turbo_circuit = df_turbo_circuit.fillna(0)

    df_hybrid_circuit = df_hybrid.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
    df_hybrid_circuit = df_hybrid_circuit.pivot(index=['circuit', 'status'], columns='year', values='counts')
    df_hybrid_circuit = df_hybrid_circuit.fillna(0)

    # reindex the dataframes with the ligroups
    df_turbo_circuit = df_turbo_circuit.reindex(ligroups, level=1, fill_value=0)
    df_hybrid_circuit = df_hybrid_circuit.reindex(ligroups, level=1, fill_value=0)

    # sort the dataframes by the index
    df_turbo_circuit.sort_index(inplace=True)
    df_hybrid_circuit.sort_index(inplace=True)

    for circuit in df_turbo_circuit.index.get_level_values(0).unique():
        plt.title('Correlation between Turbo and Hybrid era (' + str(circuit) + ')')
        plt.ylabel('Correlation')
        plt.xlabel('Compared Years')
        plt.xticks(np.arange(1, 11, 1), [str(x) + '-' + str(x + 37) for x in range(1977, 1987)])
        plt.yticks(np.arange(-1.1, 1.1, 0.1))
        plt.ylim(-1, 1)
        plt.plot(df_turbo_circuit.loc[circuit].corrwith(df_hybrid_circuit.loc[circuit]), marker='o')
        plt.savefig(os.path.join(circuitpath, 'correlation_turbo_hybrid_' + str(circuit) + '.png'))
        plt.clf()
    
    print('Analysis done')

if 't' in args:
     # check if data is already in data folder else exit
    if not os.path.exists(os.path.join(path,r'turbo_era.csv')) or not os.path.exists(os.path.join(path,r'hybrid_era.csv')):
        exit('Data not found, please run main.py with the u argument first')

    # get both datasets
    df_turbo = pd.read_csv(os.path.join(path,r'turbo_era.csv'))
    df_hybrid = pd.read_csv(os.path.join(path,r'hybrid_era.csv'))
    
    #########################################################
    ### Data preperation
    #########################################################

    # drop the finished status rows
    df_turbo = df_turbo[df_turbo['status'] != 'Finished']
    df_hybrid = df_hybrid[df_hybrid['status'] != 'Finished']
    df_turbo = df_turbo[df_turbo['status'] != 'Not classified']
    df_hybrid = df_hybrid[df_hybrid['status'] != 'Not classified']

    # filter data for only circuits in the list
    df_turbo = df_turbo[df_turbo['circuit'].isin(licircuits)]
    df_hybrid = df_hybrid[df_hybrid['circuit'].isin(licircuits)]

    # drop the years 1987 and 1988
    df_turbo = df_turbo[df_turbo['year'] != 1987]
    df_turbo = df_turbo[df_turbo['year'] != 1988]
    
    # replace year with number
    df_turbo['year'] = df_turbo['year'].replace({1977: 1, 1978: 2, 1979: 3, 1980: 4, 1981: 5, 1982: 6, 1983: 7, 1984: 8, 1985: 9, 1986: 10})
    df_hybrid['year'] = df_hybrid['year'].replace({2014: 1, 2015: 2, 2016: 3, 2017: 4, 2018: 5, 2019: 6, 2020: 7, 2021: 8, 2022: 9, 2023: 10})

    #########################################################
    ### ANOVA test
    #########################################################
    from scipy.stats import f_oneway
    
    # get the data for each year
    df_turbo_ys = df_turbo.groupby(['year', 'status']).size().reset_index(name='counts')
    df_turbo_ys = df_turbo_ys.pivot(index=['status'], columns='year', values='counts')
    df_turbo_ys = df_turbo_ys.fillna(0)
    
    df_hybrid_ys = df_hybrid.groupby(['year', 'status']).size().reset_index(name='counts')
    df_hybrid_ys = df_hybrid_ys.pivot(index=['status'], columns='year', values='counts')
    df_hybrid_ys = df_hybrid_ys.fillna(0)

    # get the data for each circuit
    df_turbo_circuit = df_turbo.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
    df_turbo_circuit = df_turbo_circuit.pivot(index=['circuit', 'status'], columns='year', values='counts')
    df_turbo_circuit = df_turbo_circuit.fillna(0)
    
    df_hybrid_circuit = df_hybrid.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
    df_hybrid_circuit = df_hybrid_circuit.pivot(index=['circuit', 'status'], columns='year', values='counts')
    df_hybrid_circuit = df_hybrid_circuit.fillna(0)
    
    # apply the ANOVA test to the data
    print('ANOVA test for each year:')
    for year in df_hybrid_ys.columns:
        print('Year: ' + str(year))
        print(f_oneway(df_turbo_ys[year], df_hybrid_ys[year]))
        print()
        
    print('ANOVA test for each circuit:')
    for circuit in df_turbo_circuit.index.get_level_values(0).unique():
        print('Circuit: ' + str(circuit))
        print(f_oneway(df_turbo_circuit.loc[circuit], df_hybrid_circuit.loc[circuit]))
        print()

    # T-test
    from scipy.stats import ttest_ind

    # apply the T-test to the data
    print('T-test for each year:')
    for year in df_hybrid_ys.columns:
        print('Year: ' + str(year))
        print(ttest_ind(df_turbo_ys[year], df_hybrid_ys[year]))
        print()

    print('T-test for each circuit:')
    for circuit in df_turbo_circuit.index.get_level_values(0).unique():
        print('Circuit: ' + str(circuit))
        print(ttest_ind(df_turbo_circuit.loc[circuit], df_hybrid_circuit.loc[circuit]))
        print()
    