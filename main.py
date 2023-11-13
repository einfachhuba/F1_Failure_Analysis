import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from f1data import getdata
import os

# check if data is already in data folder else create it
path = os.getcwd() + r'\data'
plotpath = os.getcwd() + r'\plots'
circuitpath = os.getcwd() + r'\plots\circuits'

if not os.path.exists(os.path.join(path,r'turbo_era.csv')):
    getdata(1980, 1990).to_csv(os.path.join(path,r'turbo_era.csv'), index=False)
    getdata(2014, 2024).to_csv(os.path.join(path,r'hybrid_era.csv'), index=False)

# analysing data
for file in os.listdir(path):
    if file.endswith('.csv'):
        df_data = pd.read_csv(os.path.join(path,file))
        df_data = df_data[df_data['status'] != 'Finished']
        
        # group data by date and status
        df_data_ds = df_data.groupby(['year', 'status']).size().reset_index(name='counts')
        
        # pivot data
        df_data_ds = df_data_ds.pivot(index='year', columns='status', values='counts')
        
        # plot data with 16 different colors
        df_data_ds.plot(kind='bar', stacked=True, figsize=(15, 5), color=sns.color_palette('Paired', 32))
        if file == 'turbo_era.csv':
            plt.title('F1 Breakdowns (1980 - 1990)')
            plt.ylim(0, 300)
            plt.yticks(range(0, 300, 25))
        else:
            plt.title('F1 Breakdowns (2014 - 2024)')
            plt.ylim(0, 150)
            plt.yticks(range(0, 150, 25))

        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.legend(bbox_to_anchor=(0.9999, 1))
        plt.savefig(os.path.join(plotpath, file[:-4] + '.png'))

        # group data by circuit and status and year
        df_data_ds = df_data.groupby(['year', 'circuit', 'status']).size().reset_index(name='counts')
        
        # licircuits = ['Australian Grand Prix', 'Austrian Grand Prix', 'Belgian Grand Prix', 'Brazilian Grand Prix',
        #               'British Grand Prix', 'Canadian Grand Prix', 'Dutch Grand Prix', 'European Grand Prix',
        #               'French Grand Prix', 'German Grand Prix', 'Hungarian Grand Prix', 'Italian Grand Prix',
        #               'Japanese Grand Prix', 'Mexican Grand Prix', 'Monaco Grand Prix','Portuguese Grand Prix',
        #               'Spanish Grand Prix', 'United States Grand Prix']
        
        licircuits = ['Austrian Grand Prix', 'Belgian Grand Prix', 'British Grand Prix',
                      'Canadian Grand Prix', 'Italian Grand Prix', 'Monaco Grand Prix']
        
        # filter data for only circuits int the list
        df_data_ds = df_data_ds[df_data_ds['circuit'].isin(licircuits)]

        # pivot data for each circuit
        for circuit in df_data_ds['circuit'].unique():
            df_data_ds_circuit = df_data_ds[df_data_ds['circuit'] == circuit]
            df_data_ds_circuit = df_data_ds_circuit.pivot(index='year', columns='status', values='counts')
            
            # plot data
            df_data_ds_circuit.plot(kind='bar', stacked=True, figsize=(15, 5), color=sns.color_palette('Paired'))
            plt.title('F1 Breakdowns (' + str(circuit) + ')')
            plt.xlabel('Year')
            plt.ylabel('Amount')
            plt.ylim(0, 25)
            plt.yticks(range(0, 24, 2))
            plt.legend(bbox_to_anchor=(0.9999, 1))
            plt.savefig(os.path.join(circuitpath, file[:-4] + '_' + str(circuit) + '.png'))
            plt.close()
        