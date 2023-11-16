# F1 Carpart Grouping

This document describes the grouping of carparts in my code, which is used to
have a clear overview of the carfailures.

## Grouping

The carparts are grouped in the following way:


Group 1: **Engine**
- Engine
- Injection
- Throttle
- Power Unit
- Power loss
<br/>

Group 2: **Gearbox**
- Gearbox
- Transmission
- Clutch
<br/>

Group 3: **Turbo**
- Turbo
<br/>

Group 4: **Powertrain**
- Clutch
- Halfshaft
- Differential
- CV joint
- Driveshaft
- Drivetrain
<br/>

Group 5: **Suspension**
- Suspension
- Handling
- Steering
- Vibrations
<br/>

Group 6: **Electrical**
- Electrical
- Ignition
- Spark plugs
- Battery
- Alternator
- Distributor
- Electronics
- ERS
<br/>

Group 7: **Tyre**
- Tyre
- Wheel
- Wheel bearing
- Puncture
- Brakes
- Wheel nut
- Technical
- Brake duct
<br/>

Group 8: **Fluid systems**
- Fuel system
- Out of fuel
- Fuel leak
- Water leak
- Oil leak
- Oil pressure
- Water pump
- Fuel pump
- Oil pump
- Hydraulics
- Water pressure
- Fuel pressure
<br/>

Group 9: **Chassis**
- Chassis
- Broken wing
- Rear wing
- Front wing
<br/>

Group 10: **Driver-Related**
- Driver unwell
- Fatal accident
- Injury
- Physical
- Injured
- Illness
- Seat

Group 11: **Overheating**
- Radiator
- Heat shield fire
- Overheating
- Mechanical
- Exhaust
- Cooling system
- Fire
<br/>

Group 12: **Accident**
- Accident
- Spun off
- Collision
- Collision damage
- Damage
<br/>

Group 13: **Finished**
- Finished
- Finisheds
<br/>

Group 14: **Not Classified**
- Not Classified
<br/>

Group 15: **Disqualified**
- Disqualified
<br/>

## Grouping in code

The grouping in my code is done by using a dictionary, which is defined in the following way:

```python
digroup_values = {
    'Engine':           {'Injection', 'Throttle', 'Power Unit', 'Power loss'},
    'Gearbox':          {'Transmission', 'Clutch'},
    'Powertrain':       {'Halfshaft', 'CV joint', 'Differential', 'Clutch', 'Driveshaft', 'Drivetrain'},
    'Suspension':       {'Steering', 'Handling', 'Vibrations'},
    'Electrical':       {'Spark plugs', 'Battery', 'Alternator', 'Distributor', 'Ignition', 'Electronics', 'ERS'},
    'Tyre':             {'Puncture', 'Wheel', 'Wheel bearing', 'Brakes', 'Wheel nut', 'Technical', 'Brake duct'},
    'Fluid systems':    {'Out of fuel', 'Fuel pump', 'Fuel leak', 'Fuel system', 'Oil leak', 'Oil pump', 'Oil pressure',
                        'Water leak', 'Water pump', 'Hydraulics', 'Water pressure', 'Fuel pressure'},
    'Chassis':          {'Broken wing', 'Rear wing', 'Front wing', 'Debris', 'Undertray'},
    'Driver-related':   {'Driver unwell', 'Injured', 'Injury', 'Physical', 'Fatal accident', 'Illness', 'Seat'},
    'Overheating':      {'Heat shield fire', 'Radiator', 'Mechanical', 'Exhaust', 'Cooling system', 'Fire'},
    'Accident':         {'Collision', 'Spun off', 'Collision damage', 'Damage'},
    'Finished':         {'Finisheds'}
}
```
At the groupd "Finished" we will also include all the data where the status is something like "+1 Lap", "+2 Laps", etc. since the drivers finished the race. The dictionary is used to then filter all the data in the status column of the dataframe. This is done by using the following code:

```python
dfresult['status'] = dfresult['status'].str.replace(r'\+\d{1,} Lap', 'Finished', regex=True)

for key, value in digroup_values.items():
    dfresult.loc[dfresult['status'].isin(value), 'status'] = key
```