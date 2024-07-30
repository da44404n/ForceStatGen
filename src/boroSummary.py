from pandas import concat
from pandas import DataFrame
from pandas import Series
import calculations

def calcLevelsBS(boro, currentIncidentPeriod, previousIncidentPeriod,
                    currentIncidentYTD, previousIncidentYTD):

    allBoroCurrentPeriodLevels, allBoroCurrentPeriodPercentLevels = calculations.levelsBreakdown(currentIncidentPeriod, 'ALLBORO')
    allBoroPreviousPeriodLevels, allBoroPreviousPeriodPercentLevels = calculations.levelsBreakdown(previousIncidentPeriod, 'ALLBORO')

    allBoroCurrentYTDLevels, allBoroCurrentYTDPercentLevels = calculations.levelsBreakdown(currentIncidentYTD, 'ALLBORO')
    allBoroPreviousYTDLevels, allBoroPreviousYTDPercentLevels = calculations.levelsBreakdown(previousIncidentYTD, 'ALLBORO')


    boroCurrentPeriodLevels = allBoroCurrentPeriodLevels[boro]
    boroCurrentPeriodPercentLevels = allBoroCurrentPeriodPercentLevels[boro]

    boroCurrentPeriodPercentLevels.index = boroCurrentPeriodLevels.index[:-1]
    
    boroCurrentPeriodLevels = concat([boroCurrentPeriodLevels, boroCurrentPeriodPercentLevels], axis=1)

    boroCurrentPeriodLevels.columns = ['Current Period', '%']

    boroPreviousPeriodLevels = allBoroPreviousPeriodLevels[boro]
    boroPreviousPeriodPercentLevels = allBoroPreviousPeriodPercentLevels[boro]

    boroPreviousPeriodPercentLevels.index = boroPreviousPeriodLevels.index[:-1]

    boroPreviousPeriodLevels = concat([boroPreviousPeriodLevels, boroPreviousPeriodPercentLevels], axis=1)
    boroPreviousPeriodLevels.columns = ['Previous Period', '%']


    boroPeriodDiff = calculations.prevDiff(boroCurrentPeriodLevels, boroPreviousPeriodLevels)

    boroCurrentYTDLevels = allBoroCurrentYTDLevels[boro]
    boroCurrentYTDPercentLevels = allBoroCurrentYTDPercentLevels[boro]

    boroCurrentYTDPercentLevels.index = boroCurrentYTDLevels.index[:-1]

    boroCurrentYTDLevels = concat([boroCurrentYTDLevels, boroCurrentYTDPercentLevels], axis=1)
    boroCurrentYTDLevels.columns = ['Current YTD', '%']

    boroPreviousYTDLevels = allBoroPreviousYTDLevels[boro]
    boroPreviousYTDPercentLevels = allBoroPreviousYTDPercentLevels[boro]

    boroPreviousYTDPercentLevels.index = boroPreviousYTDLevels.index[:-1]

    boroPreviousYTDLevels = concat([boroPreviousYTDLevels, boroPreviousYTDPercentLevels], axis=1)
    boroPreviousYTDLevels.columns = ['Previous YTD', '%']

    boroYTDDiff = calculations.prevDiff(boroCurrentYTDLevels, boroPreviousYTDLevels)

    boroLevels = concat([boroCurrentPeriodLevels,boroPreviousPeriodLevels,boroPeriodDiff,boroCurrentYTDLevels,boroPreviousYTDLevels,boroCurrentYTDLevels,boroPreviousYTDLevels,boroYTDDiff],axis=1)

    return boroLevels

def calcBS(func, boro, currentPeriod, previousPeriod, currentArrestPeriod=None, previousArrestPeriod=None):    
    currentPeriodAllBoro : DataFrame
    previousPeriodAllBoro : DataFrame

    if func == calculations.triArrests:
        currentPeriodAllBoro = func(currentPeriod, currentArrestPeriod, 'ALLBORO')
        previousPeriodAllBoro = func(previousPeriod, previousArrestPeriod, 'ALLBORO')
    else:    
        currentPeriodAllBoro = func(currentPeriod, 'ALLBORO')
        previousPeriodAllBoro = func(previousPeriod, 'ALLBORO')

    currentPeriodBoro = DataFrame(currentPeriodAllBoro[boro])
    previousPeriodBoro = DataFrame(previousPeriodAllBoro[boro])

    currentPeriodBoro.columns = ['Current Period']

    previousPeriodBoro.columns = ['Previous Period']

    currPrevDiff = calculations.prevDiff(currentPeriodBoro,previousPeriodBoro)

    boroIncident = concat([currentPeriodBoro,previousPeriodBoro,currPrevDiff], axis=1)

    return boroIncident

def boroSummary(boro, currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
                previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
                currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD):
    
    boroDataFrames = []

    levelsBS = calcLevelsBS(boro, currentIncidentPeriod, previousIncidentPeriod, currentIncidentYTD, previousIncidentYTD)
    levelsBS.index.name = 'FORCE LEVELS' #CHANGE THE INDEX TO CORRESPOND TO THE TABLE TITLE IN THE POWERPOINT
    boroDataFrames.append(levelsBS)

    dowBS = calcBS(calculations.dow, boro, currentIncidentPeriod, previousIncidentPeriod)
    dowBS.index.name = 'DAYS OF WEEK'
    boroDataFrames.append(dowBS)

    platoonBS = calcBS(calculations.platoon, boro, currentIncidentPeriod, previousIncidentPeriod)
    platoonBS.index.name = 'PLATOON'
    boroDataFrames.append(platoonBS)

    velocityBS = calcBS(calculations.velocity, boro, currentIncidentPeriod, previousIncidentPeriod)
    velocityBS.index.name = 'VELOCITY'
    boroDataFrames.append(velocityBS)

    injMosBS = calcBS(calculations.injuredMOS, boro, currentInteractionPeriod, previousInteractionPeriod)
    injMosBS.index.name = 'INJURED MOS'
    boroDataFrames.append(injMosBS)

    triArrestsBS = calcBS(calculations.triArrests, boro, currentIncidentPeriod, previousIncidentPeriod, currentArrestPeriod, previousArrestPeriod)
    triArrestsBS.index.name = 'TRIs WITH ARREST'
    boroDataFrames.append(triArrestsBS)

    weaponsBS = calcBS(calculations.weapons, boro, currentInteractionPeriod, previousInteractionPeriod)
    weaponsBS.index.name = 'FORCE USED BY MOS'
    boroDataFrames.append(weaponsBS)

    level2BS = calcBS(calculations.level2, boro, currentIncidentPeriod, previousIncidentPeriod)
    level2BS.index.name = 'LEVEL 2'
    boroDataFrames.append(level2BS)

    return boroDataFrames


