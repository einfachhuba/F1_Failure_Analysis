from pyergast import pyergast as pyd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dfturbo_era = pd.DataFrame()

for year in range(1980, 1989):
    df_schedule = pyd.get_schedule(year)
    inrace_amount = df_schedule['round'].count()
    for race in range(1, inrace_amount + 1):
        if dfturbo_era.empty:
            dfturbo_era = pyd.get_race_result(year, race)[['constructor', 'status']]
            dfturbo_era['date'] = df_schedule[df_schedule['round'] == str(race)]['date'].values[0]
            dfturbo_era['circuit'] = df_schedule[df_schedule['round'] == str(race)]['raceName'].values[0]
            dfturbo_era['year'] = year
            dfturbo_era['race'] = race
        else:
            dftemp = pyd.get_race_result(year, race)[['constructor', 'status']]
            dftemp['date'] = df_schedule[df_schedule['round'] == str(race)]['date'].values[0]
            dftemp['circuit'] = df_schedule[df_schedule['round'] == str(race)]['raceName'].values[0]
            dftemp['year'] = year
            dftemp['race'] = race
            dfturbo_era = pd.concat([dfturbo_era, dftemp])

print(dfturbo_era.shape)

# dropping rows with status that are not relevant
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Did not qualify']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Did not prequalify']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Retired']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Withdrew']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Excluded']

digroup_values = {
    'Engine': {'Injection', 'Throttle'},
    'Gearbox': {'Transmission', 'Clutch'},
    'Powertrain': {'Halfshaft', 'CV joint', 'Differential', 'Clutch', 'Driveshaft'},
    'Suspension': {'Steering', 'Handling', 'Vibrations'},
    'Electrical': {'Spark plugs', 'Battery', 'Alternator', 'Distributor', 'Ignition'},
    'Tyre': {'Puncture', 'Wheel', 'Wheel bearing', 'Brakes'},
    'Fluid systems': {'Out of fuel', 'Fuel pump', 'Fuel leak', 'Fuel system', 'Oil leak', 'Oil pump', 'Oil pressure',
                      'Water leak', 'Water pump', 'Hydraulics'},
    'Chassis': {'Broken wing'},
    'Driver-related': {'Driver unwell', 'Injured', 'Injury', 'Physical', 'Fatal accident'},
    'Overheating': {'Heat shield fire', 'Radiator'},
    'Accident': {'Collision', 'Spun off'},
    'Finished': {'Finisheds'}
}

# replacing some status values with more general ones
dfturbo_era['status'] = dfturbo_era['status'].str.replace(r'\+\d{1,} Lap', 'Finished', regex=True)

for key, value in digroup_values.items():
    dfturbo_era.loc[dfturbo_era['status'].isin(value), 'status'] = key

print(dfturbo_era.head())
print(dfturbo_era.shape)
print(dfturbo_era['status'].value_counts())

# new dataframe with only failures
dfturbo_era_failures = dfturbo_era[dfturbo_era['status'] != 'Finished']

# plotting
plt.figure(figsize=(20, 10))
plt.title('Turbo Era (1980-1989) - F1 Car Failures')
plt.xlabel('Failure Type')
plt.ylabel('Number of Failures')
sns.countplot(x='status', data=dfturbo_era_failures, order=dfturbo_era_failures['status'].value_counts().index)

# save plot as image
plt.savefig('turbo_era.png')


