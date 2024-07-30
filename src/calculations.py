from pandas import DataFrame
from pandas import concat
from numpy import isnan
from numpy import nan

def fstringToInt(string):
    if type(string) is not str or (type(string) is int and string < 0):
        return string
    return int(string.replace(',', '').replace('%', ''))

def handlePercent(string):
    if(type(string) is str and '%' in string):
        return None
    return string

def handleDivide(numerator, denominator):
    if isnan(numerator) or isnan(denominator):
        return None
    if denominator == 0:
        # return (f'{nan : .0%}') # this doesn't work with the replace function for some reason
        return '***'
    return (f"{(numerator / denominator) : .0%}")

def prevDiff(curr, prev):
    if curr.empty or prev.empty:
        return DataFrame()

    currCol = curr['Current Period'] if "Current Period" in curr else curr['Current YTD']
    prevCol = prev['Previous Period'] if "Previous Period" in prev else prev['Previous YTD']
    currPrevDiffCW = DataFrame(columns=['% Diff', 'Curr-Prev'])


    # currPrevDiffCW['Curr-Prev'] = currCol.apply(handlePercent).apply(fstringToInt) - prevCol.apply(handlePercent).apply(fstringToInt)
    currPrevDiffCW['Curr-Prev'] = currCol.apply(fstringToInt) - prevCol.apply(fstringToInt)


    # currPrevDiffCW['% Diff'] = (currPrevDiffCW['Curr-Prev']
    #                             .apply(handlePercent)
    #                             .apply(fstringToInt)
    #                             .combine(prevCol.apply(handlePercent).apply(fstringToInt), handleDivide)
    #                             )
    
    currPrevDiffCW['% Diff'] = (currPrevDiffCW['Curr-Prev']
                                .apply(fstringToInt)
                                .combine(prevCol.apply(fstringToInt), handleDivide))


    # currPrevDiffCW['% Diff'] = currPrevDiffCW['% Diff'].replace('inf%', '***')
    # currPrevDiffCW['% Diff'] = currPrevDiffCW['% Diff'].replace('nan%', '***')

    # currPrevDiffCW['Curr-Prev'] = currPrevDiffCW['Curr-Prev'].replace('nan', '***')
    # currPrevDiffCW['Curr-Prev'] = currPrevDiffCW['Curr-Prev'].replace('inf', '***')

    return currPrevDiffCW

def levelsBreakdown(period, group):
    if period.empty:
        return DataFrame()

    thisPeriod = period.groupby(by=group, observed=False).agg(
        Level1=('Current Incident Level1', 'sum'),
        Level2=('Current Incident Level2', 'sum'),
        Level3=('Current Incident Level3', 'sum'),
        Level4=('Current Incident Level4', 'sum')
    ) 

    # Calculate the total and percentages
    thisPeriod.columns = ['Level 1', 'Level 2', 'Level 3', 'Level 4']
    total_incidents = thisPeriod[['Level 1', 'Level 2', 'Level 3', 'Level 4']].sum(axis=1)
    thisPeriod['TOTAL'] = total_incidents

    percentDF= DataFrame(columns=['% OF LEVEL 1','% OF LEVEL 2','% OF LEVEL 3','% OF LEVEL 4'])
    percentDF['% OF LEVEL 1'] = (thisPeriod['Level 1'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['% OF LEVEL 2'] = (thisPeriod['Level 2'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['% OF LEVEL 3'] = (thisPeriod['Level 3'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['% OF LEVEL 4'] = (thisPeriod['Level 4'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF = percentDF.T

    # Transpose and rename the columns
    thisPeriod = thisPeriod.T
    return thisPeriod,percentDF

def levelsSummary(period, group='CW'):
    if period.empty:
        return DataFrame()

    thisPeriod = period.groupby(group).agg(
        Level1=('Current Incident Level1', 'sum'),
        Level2=('Current Incident Level2', 'sum'),
        Level3=('Current Incident Level3', 'sum'),
        Level4=('Current Incident Level4', 'sum')
    )

    # Calculate the total and percentages
    total_incidents = thisPeriod[['Level1', 'Level2', 'Level3', 'Level4']].sum(axis=1)
    thisPeriod['TOTAL'] = total_incidents

    percentDF= DataFrame(columns=['Level1', 'Level2', 'Level3', 'Level4'])
    percentDF['Level1'] = (thisPeriod['Level1'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['Level2'] = (thisPeriod['Level2'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['Level3'] = (thisPeriod['Level3'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF['Level4'] = (thisPeriod['Level4'] / total_incidents).apply(lambda x: f"{x:.0%}")
    percentDF = percentDF.T

    # Transpose and rename the columns
    thisPeriod = thisPeriod.T
    thisPeriod = concat([thisPeriod, percentDF], axis=1)
    return thisPeriod

def dow(period, group):
    if period.empty:
        return DataFrame()
    
    thisPeriod = period.groupby(by=group, observed=False).agg(
        MON = ('MONDAY', 'sum'),
        TUES = ('TUESDAY', 'sum'),
        WED = ('WEDNESDAY', 'sum'),
        THURS = ('THURSDAY', 'sum'),
        FRI = ('FRIDAY', 'sum'),
        SAT = ('SATURDAY', 'sum'),
        SUN = ('SUNDAY', 'sum'),
    )

    thisPeriod['TOTAL'] = thisPeriod[['MON','TUES','WED','THURS','FRI','SAT','SUN']].sum(axis=1)

    thisPeriod = thisPeriod.T
    return thisPeriod

def platoon(period, group):
    if period.empty:
        return DataFrame()

    # Summarize platoon data
    thisPeriod = period.groupby(by=group, observed=False).agg(
        First=('FIRST', 'sum'),
        Second=('SECOND', 'sum'),
        Third=('THIRD', 'sum')
    )

    # Transpose the DataFrame for the desired format
    thisPeriod = thisPeriod.T

    return thisPeriod

def velocity(period, group):
    if period.empty:
        return DataFrame()

    thisPeriod = period.groupby(by=group, observed=False).agg(
        OTC=('OccToCre', 'mean'),
        CTS=('CreToEnd','mean'),
        TOTAL= ('IncidentCount', 'sum')
    )

    thisPeriod['OTC'] = round(thisPeriod['OTC'],0).astype(int)
    thisPeriod['CTS'] = round(thisPeriod['CTS'],0).astype(int)

    thisPeriod = thisPeriod.T
    return thisPeriod

def subjectInjuryLevels(period, group):
    if period.empty:
        return DataFrame()
    
    thisPeriod = period.groupby(by=group, observed=False).agg(
        NO_INJURY = ('Max Subject Injury No Level', 'sum'),
        LEVEL_1 = ('Max Subject Injury Level1', 'sum'),
        LEVEL_2 = ('Max Subject Injury Level2', 'sum'),
        LEVEL_3 = ('Max Subject Injury Level3', 'sum'),
        LEVEL_4 = ('Max Subject Injury Level4', 'sum'),
    )

    thisPeriod['TOTAL'] = thisPeriod[['NO_INJURY', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4']].sum(axis=1)
    thisPeriod['% of NO INJURY'] = (thisPeriod['NO_INJURY'] / thisPeriod['TOTAL']).apply(lambda x: f"{x:.0%}")

    thisPeriod = thisPeriod[['NO_INJURY', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', '% of NO INJURY', 'TOTAL']]

    columnNames = ['NO INJURY', 'LEVEL 1', 'LEVEL 2', 'LEVEL 3', 'LEVEL 4', '% of NO INJURY', 'TOTAL']

    thisPeriod.columns = columnNames

    thisPeriod = thisPeriod.T

    return thisPeriod

def injuredMOS(period, group):
    thisPeriod = period.groupby(by=group, observed=False).agg(
        INJURY = ('ISM YES', 'sum'),
        NO_INJURY = ('ISM NO', 'sum')
    )

    thisPeriod['TOTAL'] = thisPeriod[['INJURY', 'NO_INJURY']].sum(axis=1)

    thisPeriod['% of NO INJURY'] = (thisPeriod['INJURY'] / thisPeriod['TOTAL']).apply(lambda x: f"{x:.0%}")

    thisPeriod = thisPeriod[['INJURY', 'NO_INJURY', 'TOTAL', '% of NO INJURY']]
    columnNames = ['INJURY', 'NO INJURY', 'TOTAL', '% of NO INJURY']
    thisPeriod.columns = columnNames

    thisPeriod = thisPeriod.T   
    return thisPeriod

def reasonForce(period, group):
    if period.empty:
        return DataFrame()
    
    thisPeriod = period.groupby(by=group, observed=False).agg(
        SELF = ('RMF Defense of self Flag', 'sum'),
        OTHER = ('RMF Defense of Other MOS Flag', 'sum'),
        PUBLIC = ('RMF Defense of Member of Public Flag', 'sum'),
        SELFHARM = ('RMF Stop Self Inflicted Harm Flag', 'sum'),
        FLEEING = ('RMF Fleeing Suspect Flag', 'sum'),
        RESISTANCE = ('RMF Overcome Resistance or Aggresion Flag', 'sum'),
        ARMED = ('RMF Subject Armed with Weapon Flag', 'sum'),
        UNINTENTIONAL = ('RMF Unintentional Flag', 'sum')
    )

    thisPeriod['TOTAL'] = thisPeriod[['SELF', 'OTHER', 'PUBLIC', 'SELFHARM', 'FLEEING', 'RESISTANCE', 'ARMED', 'UNINTENTIONAL']].sum(axis=1)

    columnNames = ['DEFENSE OF SELF', 'DEFENSE OF OTHER MOS', 'DEFENSE OF PUBLIC', 'STOP SELF-INFLICTED HARM', 'FLEEING SUSPECT', 'RESISTANCE/ AGGRESSION',
                   'SUBJECT ARMED W/WEAPON', 'UNINTENTIONAL', 'TOTAL']
    
    thisPeriod.columns = columnNames

    thisPeriod = thisPeriod.T
    return thisPeriod

def triArrests(period, arrestPeriod, group):
    if period.empty:
        return DataFrame()

    thisPeriod = period.groupby(by=group, observed=False).agg(
        TRICount=('IncidentCount', 'sum'),
        TRIwArrest=('Arrest Made Flag', 'sum'),
        ArrestForce=('ArrFor', 'sum')
    )

    thisArrestPeriod = arrestPeriod.groupby(by=group, observed=False).agg(
        ArrestCount=('ArrestCount', 'sum')
    )

    thisPeriod = concat([thisPeriod, thisArrestPeriod], axis=1)

    thisPeriod['% of Arrests'] = (thisPeriod['ArrestForce'] / thisPeriod['ArrestCount']).apply(lambda x: f"{x:.0%}")

    thisPeriod.columns = ['Total TRIs', 'TRIs w/ Arrests', 'TRIs w/ Arrests where MOS used force', 'Arrests', '% of Total Arrests']

    thisPeriod = thisPeriod.T
    return thisPeriod

def weapons(period, group):
    if period.empty:
        return DataFrame()
    
    thisPeriod = period.groupby(by=group, observed=False).agg(
        Physical = ('PhysicalForce', 'sum'),
        CEW = ('CEW', 'sum'),
        OCSpray = ('OCSpray', 'sum'),
        ImpactWeapon = ('ImpactWeapon', 'sum'),
        FireArm = ('FireArm', 'sum')
    )


    thisPeriod['TOTAL'] = thisPeriod[['Physical','CEW','OCSpray','ImpactWeapon','FireArm']].sum(axis=1)
    thisPeriod['% of Physical Force'] = (thisPeriod['Physical'] / thisPeriod['TOTAL']).apply(lambda x: f"{x:.0%}")

    thisPeriod.columns = ['Physical', 'CEW', 'OCSpray', 'Impact Weapon', 'Firearm', 'TOTAL', '% of Physical Force']
    thisPeriod = thisPeriod.T
    return thisPeriod

def boe(period, group):
    if period.empty:
        return DataFrame()
    
    thisPeriod = period.groupby(by=group, observed=False).agg(
        CRIME = ('Encounter Type Description CRIME', 'sum'),
        EDP = ('Encounter Type Description EDP', 'sum'),
        PRISONER = ('Encounter Type Description PRISONER', 'sum'),
        OTHER = ('Encounter Type Description OTHER', 'sum'),
        VTL = ('Encounter Type Description VTL', 'sum'),
        CROWD = ('Encounter Type Description CROWD', 'sum'),
        PASTCRIME = ('Encounter Type Description PASTCRIME', 'sum'),
        WANTED = ('Encounter Type Description WANTED', 'sum'),
        CUSTODY = ('Encounter Type Description CUSTODY', 'sum'),
        SUSPACTIVITY = ('Encounter Type Description SUSPACTIVITY', 'sum'),
        TRANSIT = ('Encounter Type Description TRANSIT', 'sum'),
        DETECTIVE = ('Encounter Type Description DETECTIVE', 'sum'),
        NONCRIMECALL = ('Encounter Type Description NONCRIMECALL', 'sum'),
        OOP = ('Encounter Type Description OOP', 'sum'),
        WARRANT = ('Encounter Type Description WARRANT', 'sum'),
        ANIMAL = ('Encounter Type Description ANIMAL', 'sum'),
        HOSTAGE = ('Encounter Type Description HOSTAGE', 'sum'),
        AMBUSH = ('Encounter Type Description AMBUSH', 'sum'),
        HOME = ('Encounter Type Description HOME', 'sum')
    )
    
    thisPeriod['TOTAL'] = thisPeriod[['CRIME', 'EDP', 'PRISONER', 'OTHER', 'VTL', 'CROWD', 'PASTCRIME', 'WANTED', 'SUSPACTIVITY', 'CUSTODY', 'TRANSIT', 'OOP', 'DETECTIVE', 'NONCRIMECALL', 'AMBUSH', 'HOSTAGE', 'WARRANT']].sum(axis=1)

    thisPeriod['% CRIME'] = ( (thisPeriod['CRIME']) / thisPeriod['TOTAL'] ).apply(lambda x: f"{x:.0%}")

    thisPeriod['% EDP'] = ( (thisPeriod['EDP']) / thisPeriod['TOTAL'] ).apply(lambda x: f"{x:.0%}")

    thisPeriod['% PRISONER'] = ( (thisPeriod['PRISONER']) / thisPeriod['TOTAL'] ).apply(lambda x: f"{x:.0%}")

    thisPeriod['% OTHER'] = ( (thisPeriod['OTHER']) / thisPeriod['TOTAL'] ).apply(lambda x: f"{x:.0%}")

    thisPeriod = thisPeriod[['CRIME', '% CRIME', 'EDP', '% EDP', 'PRISONER', '% PRISONER', 'OTHER', '% OTHER', 'VTL', 'CROWD', 'PASTCRIME',
                            'WANTED', 'CUSTODY', 'SUSPACTIVITY', 'TRANSIT', 'DETECTIVE', 'NONCRIMECALL', 'OOP', 'WARRANT', 'ANIMAL', 'HOSTAGE', 'AMBUSH', 'HOME', 'TOTAL']]

    thisPeriod.rename(columns={'CRIME' : 'CRIME/VIO IN PROGRESS', 'VTL' : 'VTL INFRACTION', 'CROWD' : 'CROWD CONTROL', 'PASTCRIME' : 'PAST CRIME/VIOLATION',
                            'WANTED' : 'WANTED SUSP', 'CUSTODY' : 'IN CUSTODY INJ', 'SUSPACTIVITY' : 'SUSP ACTIVITY', 'TRANSIT' : 'TRANSIT EJECTION',
                            'DETECTIVE' : 'DET INVEST', 'NONCRIMECALL' : 'NON-CRIME CALLS', 'WARRANT' : 'SEARCH WARRANT', 'ANIMAL' : 'ANIMAL COND',
                            'HOSTAGE' : 'HOSTAGE/ BAR', 'AMBUSH' : 'AMBUSH OF MOS', 'HOME' : 'HOME VISIT'})

    thisPeriod = thisPeriod.T

    return thisPeriod

def level2(period, group='CW'):
    if period.empty:
        return DataFrame()

    thisPeriod = period.groupby(group).agg(
        Allegation = ('AllegationLevel2', 'sum'),
        Prohibited = ('ProhibitedLevel2', 'sum'),
        Level2 = ('Current Incident Level2', 'sum')
    )

    thisPeriod['% Alleg Level2']  = (thisPeriod['Allegation'] / thisPeriod['Level2']).apply(lambda x: f"{x:.0%}")

    thisPeriod= thisPeriod.T
    return thisPeriod