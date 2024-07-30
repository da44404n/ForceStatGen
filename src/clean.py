from pandas import Categorical
from pandas import CategoricalDtype
from pandas import DataFrame
from pandas import to_numeric
from pandas import to_datetime
from numpy import where

def clean_boro_other(boro, category):
    if boro.startswith('PB'):
        return 'PSB'
    elif boro in category:
        return boro
    else:
        return 'OTHER'
    
def clean_boro_allboro(boro, category, boros=['PBMS', 'PBMN', 'PBBX', 'PBBS', 'PBBN', 'PBQS', 'PBQN', 'PBSI']):
    if boro in boros or boro in category:
        return boro
    else:
        return 'OTHER'


boros = ['PBMS', 'PBMN', 'PBBX', 'PBBS', 'PBBN', 'PBQS', 'PBQN', 'PBSI']

category = ['PSB','HB', 'TB', 'DB', 'CSO']

def cleanINCALL(INCALL : DataFrame):
    # converting create timestamp to a datetime object
    INCALL['Create Timestamp'] = to_datetime(INCALL['Create Timestamp']).dt.date

    # converting OccToCre to a numeric object
    INCALL['OccToCre'] = to_numeric(INCALL['OccToCre'], errors='coerce')

    # converting tri incident number to numeric then to character
    INCALL['TRI Incident Number'] = to_numeric(INCALL['TRI Incident Number'], errors='coerce').astype(str)

    # cleaning the psb key
    INCALL['BORO'] = INCALL['BORO'].astype(str)
    INCALL['PSB'] = where(INCALL['BORO'].isin(boros), INCALL['BORO'], '')

    INCALL['PSB'] = INCALL['PSB'].astype(CategoricalDtype(categories=['PBMS', 'PBMN', 'PBBX', 'PBBS', 'PBBN', 'PBQS', 'PBQN', 'PBSI'], ordered=True))

    # Apply the determined category for both 'OTHER' and 'ALLBORO' columns
    INCALL['OTHER'] = INCALL['BORO'].apply(lambda x: clean_boro_other(x, category))
    # INCALL['OTHER'] = INCALL['OTHER'].astype(CategoricalDtype(categories=category, ordered=True))

    INCALL['ALLBORO'] = INCALL['BORO'].apply(lambda x: clean_boro_allboro(x, category))

    # SETTING CATEGORIES
    INCALL['CW'] = 'CityWide'

    INCALL['Day Of The Week'] = INCALL['Day Of The Week'].astype(CategoricalDtype(categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in daysofweek:
        column_name = day.upper()
        INCALL[column_name] = where(INCALL['Day Of The Week'] == day, 1, 0)

    platoons = ['First', 'Second', 'Third']
    for platoon in platoons:
        column_name = platoon.upper()
        INCALL[column_name] = where(INCALL['Platoon'] == platoon, 1, 0)

    INCALL['Platoon'] = INCALL['Platoon'].astype(CategoricalDtype(categories=['First','Second','Third']))

    INCALL['Current Incident Level'] = INCALL['Current Incident Level'].astype(CategoricalDtype(categories=['LEVEL1', 'LEVEL2', 'LEVEL3','LEVEL4']))
    # set incident levels
    # INCALL['Current Incident Level1'] = INCALL['Current Incident Level1'] = where(INCALL['Current Incident Level'] == 'LEVEL1', 1, 0)
    levels = ['Level1', 'Level2', 'Level3', 'Level4']
    for level in levels:
        column_name = f'Current Incident {level}'
        INCALL[column_name] = where(INCALL['Current Incident Level'] == (level.upper()), 1, 0)

    # Category for injury level
    INCALL['Max Subject Injury Level'] = INCALL['Max Subject Injury Level'].astype(CategoricalDtype(categories=['No Injury', 'Level 1', 'Level 2', 'Level 3','Level 4']))

    # set injury levels
    levelDesc = ['Level 1', 'Level 2', 'Level 3','Level 4', 'No Injury']
    levels = ['Level1', 'Level2', 'Level3', 'Level4', 'No Level']
    for level in levels:
        column_name = f'Max Subject Injury {level}'
        INCALL[column_name] = where(INCALL['Max Subject Injury Level'] == levelDesc[levels.index(level)], 1, 0)

    # set encounter type descriptionLevel
    INCALL['Encounter Type Description'] = INCALL['Encounter Type Description'].astype(CategoricalDtype(categories=['CRIME/VIOLATION IN PROGRESS', 'EDP', 'PRISONER', 'OTHER (SPECIFY)','AMBUSH OF MEMBER', 'ANIMAL CONDITION', 'CROWD CONTROL', 'DETECTIVE INVESTIGATION', 'HOME VISIT', 'HOSTAGE/BARRICADED', 'IN CUSTODY INJURY', 'NON-CRIME CALLS FOR SERVICE', 'ORDER OF PROTECTION', 'PAST CRIME/VIOLATION', 'SEARCH WARRANT', 'SUSPICIOUS ACTIVITY (IF SO, SPECIFY CRIME SUSPECTED)', 'TRANSIT EJECTION', 'VTL INFRACTION', 'WANTED SUSPECT (E.G. WARRANT, I CARD)']))

    # set encounter type descriptionLevel
    levelDesc = ['CRIME/VIOLATION IN PROGRESS', 'EDP', 'PRISONER', 'OTHER (SPECIFY)','AMBUSH OF MEMBER', 'ANIMAL CONDITION', 'CROWD CONTROL', 'DETECTIVE INVESTIGATION', 'HOME VISIT', 'HOSTAGE/BARRICADED', 'IN CUSTODY INJURY', 'NON-CRIME CALLS FOR SERVICE', 'ORDER OF PROTECTION', 'PAST CRIME/VIOLATION', 'SEARCH WARRANT', 'SUSPICIOUS ACTIVITY (IF SO, SPECIFY CRIME SUSPECTED)', 'TRANSIT EJECTION', 'VTL INFRACTION', 'WANTED SUSPECT (E.G. WARRANT, I CARD)']
    levels = ['CRIME', 'EDP', 'PRISONER', 'OTHER','AMBUSH', 'ANIMAL', 'CROWD', 'DETECTIVE', 'HOME', 'HOSTAGE', 'CUSTODY', 'NONCRIMECALL', 'OOP', 'PASTCRIME', 'WARRANT', 'SUSPACTIVITY', 'TRANSIT', 'VTL', 'WANTED']
    for level in levels:
        column_name = f'Encounter Type Description {level}'
        INCALL[column_name] = where(INCALL['Encounter Type Description'] == levelDesc[levels.index(level)], 1, 0)

    INCALL['TRI Received Description'] = INCALL['TRI Received Description'].astype(CategoricalDtype(categories=['RADIO', 'PICK-UP', 'PCT. ASSIGNMENT', 'WALK-IN','PHONE', 'WRITTEN']))
    # set tri received descriptions
    levelDesc = ['RADIO', 'PICK-UP', 'PCT. ASSIGNMENT', 'WALK-IN','PHONE', 'WRITTEN']
    levels = ['RADIO', 'PICKUP', 'PCT', 'WALKIN','PHONE', 'WRITTEN']
    for level in levels:
        column_name = f'TRI Received Description {level}'
        INCALL[column_name] = where(INCALL['TRI Received Description'] == levelDesc[levels.index(level)], 1, 0)

    # # Convert 'Arrest.Made.Flag' and 'Force.Used' to 'Y' or 'N'
    # INCALL['Arrest Made Flag'] = where(INCALL['Arrest Made Flag'] == "Y", 'Y', 'N')
    INCALL['Arrest Made Flag'] = INCALL['Arrest Made Flag'].astype(CategoricalDtype(categories=['Y', 'N']))
    INCALL['Arrest Made Flag'] = where(INCALL['Arrest Made Flag'] == 'Y', 'Y', 'N')

    INCALL['Force Used'] = INCALL['Force Used'].astype(CategoricalDtype(categories=['Y', 'N']))
    INCALL['Force Used'] = where(INCALL['Force Used'] == 'Y', 'Y', 'N')

    # Create 'ArrFor' column based on conditions
    INCALL['ArrFor'] = where((INCALL['Arrest Made Flag'] == 'Y') & (INCALL['Force Used'] == 'Y'), 1, 0)

    # Convert 'Arrest.Made.Flag' to 1 or 0
    INCALL['Arrest Made Flag'] = where(INCALL['Arrest Made Flag'] == "Y", 1, 0)

    # Add 'IncidentCount' column and set to 1
    INCALL['IncidentCount'] = 1

    INCALL['Allegation Made'] = INCALL['Allegation Made'].astype(CategoricalDtype(categories=['Y', 'N']))
    INCALL['Allegation Made'] = where(INCALL['Allegation Made'] == 'Y', 'Y', 'N')

    INCALL['AllegationLevel2'] = where((INCALL['Allegation Made'] == 'Y') & (INCALL['Current Incident Level2'] == 1), 1, 0)

    INCALL['Action Prohib'] = INCALL['Action Prohib'].astype(CategoricalDtype(categories=['Y', 'N']))
    INCALL['Action Prohib'] = where(INCALL['Action Prohib'] == 'Y', 'Y', 'N')
    INCALL['ProhibitedLevel2'] = where((INCALL['Action Prohib'] == 'Y' )& (INCALL['Current Incident Level2'] == 1), 1, 0)

    return INCALL

def cleanINTALL(INTALL : DataFrame):
    INTALL['Create Timestamp'] = to_datetime(INTALL['Create Timestamp']).dt.date
    INTALL['TRI Incident Number'] = to_numeric(INTALL['TRI Incident Number'], errors='coerce').astype(str)

    INTALL['BORO'] = INTALL['BORO'].astype(str)
    INTALL['PSB'] = where(INTALL['BORO'].isin(boros), INTALL['BORO'], '')

    INTALL['PSB'] = INTALL['PSB'].astype(CategoricalDtype(categories=['PBMS', 'PBMN', 'PBBX', 'PBBS', 'PBBN', 'PBQS', 'PBQN', 'PBSI'], ordered=True))

    # Apply the determined category for both 'OTHER' and 'ALLBORO' columns
    INTALL['OTHER'] = INTALL['BORO'].apply(lambda x: clean_boro_other(x, category))
    # INTALL['OTHER'] = INTALL['OTHER'].astype(CategoricalDtype(categories=category, ordered=True))

    INTALL['ALLBORO'] = INTALL['BORO'].apply(lambda x: clean_boro_allboro(x, category))

    # SETTING CATEGORIES
    INTALL['CW'] = 'CityWide'
    INTALL['MOS Command Description'] = Categorical(INTALL['MOS Command Description'])

    # Convert flags to categories
    INTALL['MOS In Uniform Flag'] = Categorical(INTALL['MOS In Uniform Flag'], categories=['Y', 'N'])
    INTALL['ISM YES Flag'] = Categorical(INTALL['ISM YES Flag'], categories=['Y', 'N'])

    # Convert 'Y'/'N' flags to 1/0
    INTALL['ISM YES'] = (INTALL['ISM YES Flag'] == 'Y').astype(int)
    INTALL['ISM NO'] = (INTALL['ISM YES Flag'] == 'N').astype(int)
    INTALL['RMF Defense of self Flag'] = (INTALL['RMF Defense of self Flag'] == 'Y').astype(int)
    INTALL['RMF Defense of Other MOS Flag'] = (INTALL['RMF Defense of Other MOS Flag'] == 'Y').astype(int)
    INTALL['RMF Defense of Member of Public Flag'] = (INTALL['RMF Defense of Member of Public Flag'] == 'Y').astype(int)
    INTALL['RMF Stop Self Inflicted Harm Flag'] = (INTALL['RMF Stop Self Inflicted Harm Flag'] == 'Y').astype(int)
    INTALL['RMF Fleeing Suspect Flag'] = (INTALL['RMF Fleeing Suspect Flag'] == 'Y').astype(int)
    INTALL['RMF Overcome Resistance or Aggresion Flag'] = (INTALL['RMF Overcome Resistance or Aggresion Flag'] == 'Y').astype(int)
    INTALL['RMF Subject Armed with Weapon Flag'] = (INTALL['RMF Subject Armed with Weapon Flag'] == 'Y').astype(int)
    INTALL['RMF Unintentional Flag'] = (INTALL['RMF Unintentional Flag'] == 'Y').astype(int)
    INTALL['UNI YES'] = (INTALL['MOS In Uniform Flag'] == 'Y').astype(int)
    INTALL['UNI NO'] = (INTALL['MOS In Uniform Flag'] == 'N').astype(int)

    # Set InteractionCount to 1 for all rows
    INTALL['InteractionCount'] = 1

    # Complex conditions for PhysicalForce and CEW
    INTALL['PhysicalForce'] = ((INTALL['FMT Hand Strike Flag'] == 'Y') | 
                            (INTALL['FMT Foot Strike Flag'] == 'Y') | 
                            (INTALL['FMT Forcible Take Down'] == 'Y') | 
                            (INTALL['FMT Wrestling Grappling Flag'] == 'Y')).astype(int)

    INTALL['CEW'] = ((INTALL['FMT Conducted Electrical Weapon Drive Stun Flag'] == 'Y') | 
                    (INTALL['FMT Conducted Electrical Weapon Probes Flag'] == 'Y')).astype(int)

    # Convert remaining 'Y'/'N' flags to 1/0
    INTALL['ImpactWeapon'] = (INTALL['FMT Impact Weapon Flag'] == 'Y').astype(int)
    INTALL['FireArm'] = (INTALL['FMT Discharged Firearm Flag'] == 'Y').astype(int)
    INTALL['OCSpray'] = (INTALL['FMT OC Spray Flag'] == 'Y').astype(int)

    return INTALL

def cleanARRESTS(ARRESTS : DataFrame):
    # ARRESTS['Arrest Date'] = to_datetime(ARRESTS['Arrest Date'], format='%m/%d/%Y', errors='coerce')
    #).dt.strftime('%m/%d/%Y')
    ARRESTS['Arrest Date'] = to_datetime(ARRESTS['Arrest Date']).dt.date

    ARRESTS['Command Description'] = to_numeric(ARRESTS['Arresting_MOS_Command_Description'], errors='coerce').astype(str)

    ARRESTS['BORO'] = ARRESTS['BORO'].astype(str)
    ARRESTS['PSB'] = where(ARRESTS['BORO'].isin(boros), ARRESTS['BORO'], '')

    ARRESTS['PSB'] = ARRESTS['PSB'].astype(CategoricalDtype(categories=['PBMS', 'PBMN', 'PBBX', 'PBBS', 'PBBN', 'PBQS', 'PBQN', 'PBSI'], ordered=True))

    # Apply the determined category for both 'OTHER' and 'ALLBORO' columns
    ARRESTS['OTHER'] = ARRESTS['BORO'].apply(lambda x: clean_boro_other(x, category))
    # ARRESTS['OTHER'] = ARRESTS['OTHER'].astype(CategoricalDtype(categories=category, ordered=True))

    ARRESTS['ALLBORO'] = ARRESTS['BORO'].apply(lambda x: clean_boro_allboro(x, category))
    # ARRESTS['ALLBORO'] = ARRESTS['ALLBORO'].astype(CategoricalDtype(categories= boros + (category[1:]), ordered=True))

    ARRESTS['CW'] = 'CityWide'
    ARRESTS['ArrestCount'] = 1

    return ARRESTS
