from pyergast import pyergast as pyd
import pandas as pd

dfturbo_era = pd.DataFrame()

dirace_amount = {
    1980: 14, 1981: 15, 1982: 16, 1983: 15, 1984: 16,
    1985: 16, 1986: 16, 1987: 16, 1988: 16, 1989: 16
}

for year in range(1980, 1989):
    df_schedule = pyd.get_schedule(year)
    for race in range(1, dirace_amount[year] + 1):
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

# dropping rows with status "Did not qualify" and "Did not prequalify", since they are not relevant
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Did not qualify']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Did not prequalify']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Retired']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Withdrew']
dfturbo_era = dfturbo_era[dfturbo_era['status'] != 'Excluded']

# replacing some status values with more general ones
dfturbo_era['status'] = dfturbo_era['status'].str.replace(r'\+\d{1,} Lap', 'Finished', regex=True)
dfturbo_era['status'] = dfturbo_era['status'].replace('Injection', 'Engine')
dfturbo_era['status'] = dfturbo_era['status'].replace('Throttle', 'Engine')
dfturbo_era['status'] = dfturbo_era['status'].replace('Transmission', 'Gearbox')
dfturbo_era['status'] = dfturbo_era['status'].replace('Clutch', 'Gearbox')
dfturbo_era['status'] = dfturbo_era['status'].replace('Halfshaft', 'Powertrain')
dfturbo_era['status'] = dfturbo_era['status'].replace('CV joint', 'Powertrain')
dfturbo_era['status'] = dfturbo_era['status'].replace('Differential', 'Powertrain')
dfturbo_era['status'] = dfturbo_era['status'].replace('Clutch', 'Powertrain')
dfturbo_era['status'] = dfturbo_era['status'].replace('Driveshaft', 'Powertrain')
dfturbo_era['status'] = dfturbo_era['status'].replace('Steering', 'Suspension')
dfturbo_era['status'] = dfturbo_era['status'].replace('Handling', 'Suspension')
dfturbo_era['status'] = dfturbo_era['status'].replace('Vibrations', 'Suspension')
dfturbo_era['status'] = dfturbo_era['status'].replace('Spark plugs', 'Electrical')
dfturbo_era['status'] = dfturbo_era['status'].replace('Battery', 'Electrical')
dfturbo_era['status'] = dfturbo_era['status'].replace('Alternator', 'Electrical')
dfturbo_era['status'] = dfturbo_era['status'].replace('Distributor', 'Electrical')
dfturbo_era['status'] = dfturbo_era['status'].replace('Ignition', 'Electrical')
dfturbo_era['status'] = dfturbo_era['status'].replace('Puncture', 'Tyre')
dfturbo_era['status'] = dfturbo_era['status'].replace('Wheel', 'Tyre')
dfturbo_era['status'] = dfturbo_era['status'].replace('Wheel bearing', 'Tyre')
dfturbo_era['status'] = dfturbo_era['status'].replace('Brakes', 'Tyre')
dfturbo_era['status'] = dfturbo_era['status'].replace('Out of fuel', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Fuel pump', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Fuel leak', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Fuel system', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Oil leak', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Oil pump', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Oil pressure', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Water leak', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Water pump', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Hydraulics', 'Fluid systems')
dfturbo_era['status'] = dfturbo_era['status'].replace('Broken wing', 'Chassis')
dfturbo_era['status'] = dfturbo_era['status'].replace('Driver unwell', 'Driver-related')
dfturbo_era['status'] = dfturbo_era['status'].replace('Injured', 'Driver-related')
dfturbo_era['status'] = dfturbo_era['status'].replace('Injury', 'Driver-related')
dfturbo_era['status'] = dfturbo_era['status'].replace('Physical', 'Driver-related')
dfturbo_era['status'] = dfturbo_era['status'].replace('Fatal accident', 'Driver-related')
dfturbo_era['status'] = dfturbo_era['status'].replace('Heat shield fire', 'Overheating')
dfturbo_era['status'] = dfturbo_era['status'].replace('Radiator', 'Overheating')
dfturbo_era['status'] = dfturbo_era['status'].replace('Collision', 'Accident')
dfturbo_era['status'] = dfturbo_era['status'].replace('Spun off', 'Accident')
dfturbo_era['status'] = dfturbo_era['status'].replace('Finisheds', 'Finished')

print(dfturbo_era.head())
print(dfturbo_era.shape)


dfturbo_era_failures = dfturbo_era[dfturbo_era['status'] != 'Finished']

#create a Barchart with legend
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20, 10))
plt.title('Turbo Era (1980-1989) - F1 Car Failures')
plt.xlabel('Failure Type')
plt.ylabel('Number of Failures')
sns.countplot(x='status', data=dfturbo_era_failures, order=dfturbo_era_failures['status'].value_counts().index)

# save plot as image
plt.savefig('turbo_era.png')


