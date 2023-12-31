from pyergast import pyergast as pyd
import pandas as pd
import os

def getdata(startdate, enddate):
    dfresult = pd.DataFrame()
    today = pd.to_datetime('today').strftime('%Y-%m-%d')
    
    for year in range(startdate, enddate):
        df_schedule = pyd.get_schedule(year)
        inrace_amount = df_schedule[df_schedule['date'] < today]['round'].count()
        for race in range(1, inrace_amount + 1):
            if dfresult.empty:
                dfresult = pyd.get_race_result(year, race)[['constructor', 'status']]
                dfresult['date'] = df_schedule[df_schedule['round'] == str(race)]['date'].values[0]
                dfresult['circuit'] = df_schedule[df_schedule['round'] == str(race)]['raceName'].values[0]
                dfresult['year'] = year
                dfresult['race'] = race
            else:
                dftemp = pyd.get_race_result(year, race)[['constructor', 'status']]
                dftemp['date'] = df_schedule[df_schedule['round'] == str(race)]['date'].values[0]
                dftemp['circuit'] = df_schedule[df_schedule['round'] == str(race)]['raceName'].values[0]
                dftemp['year'] = year
                dftemp['race'] = race
                dfresult = pd.concat([dfresult, dftemp])
    
    # 2 corner cases in Hybrid Era where the status is not fully correct
    if startdate == 2014:
        if dfresult[(dfresult['year'] == 2014) & (dfresult['circuit'] == 'Malaysian Grand Prix')].empty == False:
            dfresult.loc[(dfresult['year'] == 2014) & (dfresult['circuit'] == 'Malaysian Grand Prix') & (dfresult['status'] == 'Technical'), 'status'] = 'Chassis'

        if dfresult[(dfresult['year'] == 2023) & (dfresult['circuit'] == 'Singapore Grand Prix')].empty == False:
            dfresult.loc[(dfresult['year'] == 2023) & (dfresult['circuit'] == 'Singapore Grand Prix') & (dfresult['status'] == 'Technical'), 'status'] = 'Overheating'

    dfresult = dfresult[~dfresult['status'].isin(['Did not qualify', 'Did not prequalify', 'Retired', 'Withdrew', 'Excluded', 'Mechanical', 'Not Classified'])]

    digroup_values = {
        'Engine': {'Injection', 'Throttle', 'Power Unit', 'Power loss'},
        'Gearbox': {'Transmission', 'Clutch'},
        'Powertrain': {'Halfshaft', 'CV joint', 'Differential', 'Driveshaft', 'Drivetrain'},
        'Suspension': {'Steering', 'Handling', 'Vibrations'},
        'Electrical': {'Spark plugs', 'Battery', 'Alternator', 'Distributor', 'Ignition', 'Electronics', 'ERS'},
        'Tyre': {'Puncture', 'Wheel', 'Wheel bearing', 'Brakes', 'Wheel nut', 'Technical', 'Brake duct'},
        'Fluid systems': {'Out of fuel', 'Fuel pump', 'Fuel leak', 'Fuel system', 'Oil leak', 'Oil pump', 'Oil pressure',
                        'Water leak', 'Water pump', 'Hydraulics', 'Water pressure', 'Fuel pressure', 'Fuel pipe'},
        'Chassis': {'Broken wing', 'Rear wing', 'Front wing', 'Debris', 'Undertray'},
        'Driver-related': {'Driver unwell', 'Injured', 'Injury', 'Physical', 'Fatal accident', 'Illness', 'Seat'},
        'Overheating': {'Heat shield fire', 'Radiator', 'Exhaust', 'Cooling system', 'Fire'},
        'Accident': {'Collision', 'Spun off', 'Collision damage', 'Damage'},
        'Finished': {'Finisheds'}
    }

    dfresult['status'] = dfresult['status'].str.replace(r'\+\d{1,} Lap', 'Finished', regex=True)

    for key, value in digroup_values.items():
        dfresult.loc[dfresult['status'].isin(value), 'status'] = key
        
    return dfresult
