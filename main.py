import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from f1data import getdata
import os

# check if data is already in data folder else create it
path = os.getcwd() + r'\data'
plotpath = os.getcwd() + r'\plots'
if not os.path.exists(os.path.join(path,r'turbo_era.csv')):
    getdata(1980, 1990).to_csv(os.path.join(path,r'turbo_era.csv'), index=False)
    getdata(2014, 2024).to_csv(os.path.join(path,r'hybrid_era.csv'), index=False)

# analysing data
for file in os.listdir(path):
    if file.endswith('.csv'):
        df_data = pd.read_csv(os.path.join(path,file))
        df_data = df_data[df_data['status'] != 'Finished']
        
        # group data by date and status
        df_data = df_data.groupby(['year', 'status']).size().reset_index(name='counts')
        
        # pivot data
        df_data = df_data.pivot(index='year', columns='status', values='counts')
        
        # plot data
        df_data.plot(kind='bar', stacked=True, figsize=(15, 5))
        if file == 'turbo_era.csv':
            plt.title('F1 Breakdowns (1980 - 1990)')
        else:
            plt.title('F1 Breakdowns (2014 - 2024)')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.ylim(0, 275)
        plt.yticks(range(0, 275, 25))
        plt.legend(bbox_to_anchor=(0.9999, 1))
        plt.savefig(os.path.join(plotpath, file[:-4] + '.png'))
        