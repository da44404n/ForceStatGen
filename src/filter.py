from pandas import to_datetime

from threading import Thread

# Data reset

def setTimeFrameFilter(df, dateStart, dateEnd, arrest=False):
    if arrest:
        return df[(to_datetime(df['Arrest Date']) >= dateStart) & (to_datetime(df['Arrest Date']) <= dateEnd)]
    
    return df[(to_datetime(df['Create Timestamp']) >= dateStart) & (to_datetime(df['Create Timestamp']) <= dateEnd)]

def dates(INCALL, INTALL, ARRESTS, dateStartCurr, dateEndCurr,
        dateStartPre, dateEndPre, ytdCurr, ytdPre):

    # columns for the incall period/ytd
    inc_period_ytd_selected_columns = [
        'TRI Incident Number', 'Create Timestamp', 'OccToCre', 'OccToEnd', 'CreToEnd', 'Platoon', 'Day Of The Week', 'TRI Received Description', 'Current Incident Level', 'Current Incident Level1', 'Current Incident Level2',
        'Current Incident Level3', 'Current Incident Level4', 'Encounter Type Description', 'Max Subject Injury Level', 'Max Subject Injury Level1', 'Max Subject Injury Level2', 'Max Subject Injury Level3',
        'Max Subject Injury Level4', 'Max Subject Injury No Level', 'IncidentCount',
        'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'FIRST', 'SECOND', 'THIRD',
        'Encounter Type Description CRIME', 'Encounter Type Description EDP', 'Encounter Type Description PRISONER', 'Encounter Type Description OTHER', 'Encounter Type Description AMBUSH', 'Encounter Type Description ANIMAL', 'Encounter Type Description CROWD',
        'Encounter Type Description DETECTIVE', 'Encounter Type Description HOME', 'Encounter Type Description HOSTAGE', 'Encounter Type Description CUSTODY', 'Encounter Type Description NONCRIMECALL', 'Encounter Type Description OOP', 'Encounter Type Description PASTCRIME', 
        'Encounter Type Description WARRANT', 'Encounter Type Description SUSPACTIVITY', 'Encounter Type Description TRANSIT', 'Encounter Type Description VTL', 'Encounter Type Description WANTED',
        'TRI Received Description RADIO', 'TRI Received Description PICKUP', 'TRI Received Description PCT', 'TRI Received Description WALKIN', 'TRI Received Description PHONE', 'TRI Received Description WRITTEN', 'AllegationLevel2', 'ProhibitedLevel2',
        'Arrest Made Flag', 'ArrFor', 'OWNING_COMMAND_CODE','OWNING COMMAND', 'PSB', 'OTHER', 'CW', 'ALLBORO'
    ]

    # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
    curr_inc_period_filter = setTimeFrameFilter(INCALL, dateStartCurr, dateEndCurr)
    CurrentIncidentPeriod = curr_inc_period_filter[inc_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
    curr_inc_ytd_filter = setTimeFrameFilter(INCALL, ytdCurr, dateEndCurr)
    CurrentIncidentYTD = curr_inc_ytd_filter[inc_period_ytd_selected_columns]

    # interaction period/ytd columns selected
    int_period_ytd_selected_columns = [
        'TRI Incident Number', 'TRI Interaction Number', 'Create Timestamp', 'MOS Command Code', 'MOS Command Description', 'PSB', 'OTHER', 'CW', 'ALLBORO', 'MOS In Uniform Flag', 'ISM YES', 'ISM NO', 'RMF Defense of self Flag',
        'RMF Defense of Other MOS Flag', 'RMF Defense of Member of Public Flag', 'RMF Stop Self Inflicted Harm Flag', 'RMF Fleeing Suspect Flag', 'RMF Overcome Resistance or Aggresion Flag', 'UNI YES', 'UNI NO',
        'RMF Subject Armed with Weapon Flag', 'RMF Unintentional Flag', 'InteractionCount', 'PhysicalForce', 'CEW', 'OCSpray', 'ImpactWeapon', 'FireArm'
    ]

    # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
    curr_int_period_filter = setTimeFrameFilter(INTALL, dateStartCurr, dateEndCurr)
    CurrentInteractionPeriod = curr_int_period_filter[int_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
    curr_int_ytd_filter = setTimeFrameFilter(INTALL, ytdCurr, dateEndCurr)
    CurrentInteractionYTD = curr_int_ytd_filter[int_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
    prev_inc_period_filter = setTimeFrameFilter(INCALL, dateStartPre, dateEndPre)
    PreviousIncidentPeriod = prev_inc_period_filter[inc_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
    prev_inc_ytd_filter = setTimeFrameFilter(INCALL, ytdPre, dateEndPre)
    PreviousIncidentYTD = prev_inc_ytd_filter[inc_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
    prev_int_period_filter = setTimeFrameFilter(INTALL, dateStartPre, dateEndPre)
    PreviousInteractionPeriod = prev_int_period_filter[int_period_ytd_selected_columns]

    # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
    prev_int_ytd_filter = setTimeFrameFilter(INTALL, ytdPre, dateEndPre)
    PreviousInteractionYTD = prev_int_ytd_filter[int_period_ytd_selected_columns]


    arr_period_ytd_selected_columns = [
        'Arrest Identifier', 'Arresting_MOS_Command_Code', 'Arresting_MOS_Command_Description', 'PSB', 'OTHER', 'CW', 'ALLBORO',  'ArrestCount'
    ]

    # Filter rows where 'Arrest Date' is between 'dateStartCurr' and 'dateEndCurr'
    curr_arr_period_filter = setTimeFrameFilter(ARRESTS, dateStartCurr, dateEndCurr, arrest=True)
    CurrentArrestPeriod = curr_arr_period_filter[arr_period_ytd_selected_columns]

    # curr arr ytd
    curr_arr_ytd_filter = setTimeFrameFilter(ARRESTS, ytdCurr, dateEndCurr, arrest=True)
    CurrentArrestYTD = curr_arr_ytd_filter[arr_period_ytd_selected_columns]

    prev_arr_period_filter = setTimeFrameFilter(ARRESTS, dateStartPre, dateEndPre, arrest=True)
    PreviousArrestPeriod = prev_arr_period_filter[arr_period_ytd_selected_columns]

    prev_arr_ytd_filter = setTimeFrameFilter(ARRESTS, ytdPre, dateEndPre, arrest=True)
    PreviousArrestYTD = prev_arr_ytd_filter[arr_period_ytd_selected_columns]

    return CurrentIncidentPeriod, CurrentIncidentYTD, CurrentInteractionPeriod, CurrentInteractionYTD, PreviousIncidentPeriod, PreviousIncidentYTD, PreviousInteractionPeriod, PreviousInteractionYTD, CurrentArrestPeriod, CurrentArrestYTD, PreviousArrestPeriod, PreviousArrestYTD
    # Data Reset End

# Threaded below but it makes NO DIFFERENCE in performance

# def setIncallFilter(INCALL, dateStartCurr, dateEndCurr,
#         dateStartPre, dateEndPre, ytdCurr, ytdPre, filters):
    
#     # columns for the incall period/ytd
#     inc_period_ytd_selected_columns = [
#         'TRI Incident Number', 'Create Timestamp', 'OccToCre', 'OccToEnd', 'CreToEnd', 'Platoon', 'Day Of The Week', 'TRI Received Description', 'Current Incident Level', 'Current Incident Level1', 'Current Incident Level2',
#         'Current Incident Level3', 'Current Incident Level4', 'Encounter Type Description', 'Max Subject Injury Level', 'Max Subject Injury Level1', 'Max Subject Injury Level2', 'Max Subject Injury Level3',
#         'Max Subject Injury Level4', 'Max Subject Injury No Level', 'IncidentCount',
#         'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'FIRST', 'SECOND', 'THIRD',
#         'Encounter Type Description CRIME', 'Encounter Type Description EDP', 'Encounter Type Description PRISONER', 'Encounter Type Description OTHER', 'Encounter Type Description AMBUSH', 'Encounter Type Description ANIMAL', 'Encounter Type Description CROWD',
#         'Encounter Type Description DETECTIVE', 'Encounter Type Description HOME', 'Encounter Type Description HOSTAGE', 'Encounter Type Description CUSTODY', 'Encounter Type Description NONCRIMECALL', 'Encounter Type Description OOP', 'Encounter Type Description PASTCRIME', 
#         'Encounter Type Description WARRANT', 'Encounter Type Description SUSPACTIVITY', 'Encounter Type Description TRANSIT', 'Encounter Type Description VTL', 'Encounter Type Description WANTED',
#         'TRI Received Description RADIO', 'TRI Received Description PICKUP', 'TRI Received Description PCT', 'TRI Received Description WALKIN', 'TRI Received Description PHONE', 'TRI Received Description WRITTEN', 'AllegationLevel2', 'ProhibitedLevel2',
#         'Arrest Made Flag', 'ArrFor', 'OWNING COMMAND', 'PSB', 'OTHER', 'CW', 'ALLBORO'
#     ]

#     # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
#     curr_inc_period_filter = setTimeFrameFilter(INCALL, dateStartCurr, dateEndCurr)
#     CurrentIncidentPeriod = curr_inc_period_filter[inc_period_ytd_selected_columns]
#     filters['CurrentIncidentPeriod'] = CurrentIncidentPeriod

#     # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
#     curr_inc_ytd_filter = setTimeFrameFilter(INCALL, ytdCurr, dateEndCurr)
#     CurrentIncidentYTD = curr_inc_ytd_filter[inc_period_ytd_selected_columns]
#     filters['CurrentIncidentYTD'] = CurrentIncidentYTD

#     # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
#     prev_inc_period_filter = setTimeFrameFilter(INCALL, dateStartPre, dateEndPre)
#     PreviousIncidentPeriod = prev_inc_period_filter[inc_period_ytd_selected_columns]
#     filters['PreviousIncidentPeriod'] = PreviousIncidentPeriod

#     # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
#     prev_inc_ytd_filter = setTimeFrameFilter(INCALL, ytdPre, dateEndPre)
#     PreviousIncidentYTD = prev_inc_ytd_filter[inc_period_ytd_selected_columns]
#     filters['PreviousIncidentYTD'] = PreviousIncidentYTD

#     return CurrentIncidentPeriod, CurrentIncidentYTD, PreviousIncidentPeriod, PreviousIncidentYTD

# def setIntallFilter(INTALL, dateStartCurr, dateEndCurr,
#         dateStartPre, dateEndPre, ytdCurr, ytdPre, filters):
    
#     # interaction period/ytd columns selected
#     int_period_ytd_selected_columns = [
#         'TRI Incident Number', 'TRI Interaction Number', 'Create Timestamp', 'MOS Command Description', 'PSB', 'OTHER', 'CW', 'ALLBORO', 'MOS In Uniform Flag', 'ISM YES', 'ISM NO', 'RMF Defense of self Flag',
#         'RMF Defense of Other MOS Flag', 'RMF Defense of Member of Public Flag', 'RMF Stop Self Inflicted Harm Flag', 'RMF Fleeing Suspect Flag', 'RMF Overcome Resistance or Aggresion Flag', 'UNI YES', 'UNI NO',
#         'RMF Subject Armed with Weapon Flag', 'RMF Unintentional Flag', 'InteractionCount', 'PhysicalForce', 'CEW', 'OCSpray', 'ImpactWeapon', 'FireArm'
#     ]

#     # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
#     curr_int_period_filter = setTimeFrameFilter(INTALL, dateStartCurr, dateEndCurr)
#     CurrentInteractionPeriod = curr_int_period_filter[int_period_ytd_selected_columns]
#     filters['CurrentInteractionPeriod'] = CurrentInteractionPeriod

#     # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
#     curr_int_ytd_filter = setTimeFrameFilter(INTALL, ytdCurr, dateEndCurr)
#     CurrentInteractionYTD = curr_int_ytd_filter[int_period_ytd_selected_columns]
#     filters['CurrentInteractionYTD'] = CurrentInteractionYTD

#     # Filter rows where 'Create Timestamp' is between 'dateStartCurr' and 'dateEndCurr'
#     prev_int_period_filter = setTimeFrameFilter(INTALL, dateStartPre, dateEndPre)
#     PreviousInteractionPeriod = prev_int_period_filter[int_period_ytd_selected_columns]
#     filters['PreviousInteractionPeriod'] = PreviousInteractionPeriod

#     # Filter rows where 'Create Timestamp' is between 'ytdCurr' and 'dateEndCurr'
#     prev_int_ytd_filter = setTimeFrameFilter(INTALL, ytdPre, dateEndPre)
#     PreviousInteractionYTD = prev_int_ytd_filter[int_period_ytd_selected_columns]
#     filters['PreviousInteractionYTD'] = PreviousInteractionYTD

#     return CurrentInteractionPeriod, CurrentInteractionYTD, PreviousInteractionPeriod, PreviousInteractionYTD

# def setArrestFilter(ARRESTS, dateStartCurr, dateEndCurr,
#         dateStartPre, dateEndPre, ytdCurr, ytdPre, filters):
    
#     arr_period_ytd_selected_columns = [
#         'Arrest Identifier', 'Arresting_MOS_Command_Description', 'PSB', 'OTHER', 'CW', 'ALLBORO',  'ArrestCount'
#     ]

#     # Filter rows where 'Arrest Date' is between 'dateStartCurr' and 'dateEndCurr'
#     curr_arr_period_filter = setTimeFrameFilter(ARRESTS, dateStartCurr, dateEndCurr, arrest=True)
#     CurrentArrestPeriod = curr_arr_period_filter[arr_period_ytd_selected_columns]
#     filters['CurrentArrestPeriod'] = CurrentArrestPeriod

#     # curr arr ytd
#     curr_arr_ytd_filter = setTimeFrameFilter(ARRESTS, ytdCurr, dateEndCurr, arrest=True)
#     CurrentArrestYTD = curr_arr_ytd_filter[arr_period_ytd_selected_columns]
#     filters['CurrentArrestYTD'] = CurrentArrestYTD

#     prev_arr_period_filter = setTimeFrameFilter(ARRESTS, dateStartPre, dateEndPre, arrest=True)
#     PreviousArrestPeriod = prev_arr_period_filter[arr_period_ytd_selected_columns]
#     filters['PreviousArrestPeriod'] = PreviousArrestPeriod

#     prev_arr_ytd_filter = setTimeFrameFilter(ARRESTS, ytdPre, dateEndPre, arrest=True)
#     PreviousArrestYTD = prev_arr_ytd_filter[arr_period_ytd_selected_columns]
#     filters['PreviousArrestYTD'] = PreviousArrestYTD    

#     return CurrentArrestPeriod, CurrentArrestYTD, PreviousArrestPeriod, PreviousArrestYTD

# def resetThreaded(INCALL, INTALL, ARRESTS, dateStartCurr, dateEndCurr,
#         dateStartPre, dateEndPre, ytdCurr, ytdPre):
    
#     incallFilters = {
#         'CurrentIncidentPeriod': None,
#         'CurrentIncidentYTD': None,
#         'PreviousIncidentPeriod': None,
#         'PreviousIncidentYTD': None
#     }

#     intallFilters = {
#         'CurrentInteractionPeriod': None,
#         'CurrentInteractionYTD': None,
#         'PreviousInteractionPeriod': None,
#         'PreviousInteractionYTD': None,
#     }

#     arrestsFilters = {
#         'CurrentArrestPeriod': None,
#         'CurrentArrestYTD': None,
#         'PreviousArrestPeriod': None,
#         'PreviousArrestYTD': None
#     }

#     incallThread = Thread(target=setIncallFilter, args=(INCALL, dateStartCurr, dateEndCurr, dateStartPre, dateEndPre, ytdCurr, ytdPre, incallFilters))
#     intallThread = Thread(target=setIntallFilter, args=(INTALL, dateStartCurr, dateEndCurr, dateStartPre, dateEndPre, ytdCurr, ytdPre, intallFilters))
#     arrestsThread = Thread(target=setArrestFilter, args=(ARRESTS, dateStartCurr, dateEndCurr, dateStartPre, dateEndPre, ytdCurr, ytdPre, arrestsFilters))

#     incallThread.start()
#     intallThread.start()
#     arrestsThread.start()

#     incallThread.join()
#     intallThread.join()
#     arrestsThread.join()

#     return (incallFilters['CurrentIncidentPeriod'], incallFilters['CurrentIncidentYTD'], intallFilters['CurrentInteractionPeriod'],
#     intallFilters['CurrentInteractionYTD'], incallFilters['PreviousIncidentPeriod'], incallFilters['PreviousIncidentYTD'], 
#     intallFilters['PreviousInteractionPeriod'], intallFilters['PreviousInteractionYTD'], arrestsFilters['CurrentArrestPeriod'], arrestsFilters['CurrentArrestYTD'],
#     arrestsFilters['PreviousArrestPeriod'], arrestsFilters['PreviousArrestYTD'])

