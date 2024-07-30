from pandas import DataFrame
from pandas import concat
import calculations

def calcLevelsCWS(currentIncidentPeriod, previousIncidentPeriod, currentIncidentYTD, previousIncidentYTD):
    currentPeriodLevelsCW = calculations.levelsSummary(currentIncidentPeriod, 'CW')
    currentPeriodLevelsCW.columns = ['Current Period', '%']

    previousPeriodLevelsCW = calculations.levelsSummary(previousIncidentPeriod, 'CW')
    previousPeriodLevelsCW.columns = ['Previous Period', '%']

    currPrevPeriodDiffCW = calculations.prevDiff(currentPeriodLevelsCW, previousPeriodLevelsCW)

    currentYTDLevelsCW = calculations.levelsSummary(currentIncidentYTD, 'CW')
    currentYTDLevelsCW.columns = ['Current YTD', '%']

    previousYTDLevelsCW = calculations.levelsSummary(previousIncidentYTD, 'CW')
    previousYTDLevelsCW.columns = ['Previous YTD', '%']

    currPrevYTDDiffCW = calculations.prevDiff(currentYTDLevelsCW, previousYTDLevelsCW)

    Levels_CW = concat([currentPeriodLevelsCW,previousPeriodLevelsCW,currPrevPeriodDiffCW,currentYTDLevelsCW,previousYTDLevelsCW,currPrevYTDDiffCW],axis=1)

    return Levels_CW

def calcCWS(func, currentPeriod, previousPeriod, currentArrestPeriod=None, previousArrestPeriod=None):
    currentPeriodCW : DataFrame
    previousPeriodCW : DataFrame

    if func == calculations.triArrests:
        currentPeriodCW = func(currentPeriod, currentArrestPeriod, 'CW')

        previousPeriodCW = func(previousPeriod, previousArrestPeriod, 'CW')
    else:
        currentPeriodCW = func(currentPeriod, 'CW')
        previousPeriodCW = func(previousPeriod, 'CW')

    currentPeriodCW.columns = ['Current Period']
    previousPeriodCW.columns = ['Previous Period']

    currPrevDiff = calculations.prevDiff(currentPeriodCW,previousPeriodCW)

    cwIncident = concat([currentPeriodCW,previousPeriodCW,currPrevDiff], axis=1)

    return cwIncident

def periodSummary(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
    previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
    currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD):

    summaryDataFrames = []

    levelsCW = calcLevelsCWS(currentIncidentPeriod, previousIncidentPeriod, currentIncidentYTD, previousIncidentYTD)
    levelsCW.index.name = 'FORCE LEVELS' #CHANGE THE INDEX TO CORRESPOND TO THE TABLE TITLE IN THE POWERPOINT
    summaryDataFrames.append(levelsCW)

    dowCW = calcCWS(calculations.dow, currentIncidentPeriod, previousIncidentPeriod)
    dowCW.index.name = 'DAYS OF WEEK'
    summaryDataFrames.append(dowCW)

    platoonCW = calcCWS(calculations.platoon, currentIncidentPeriod, previousIncidentPeriod)
    platoonCW.index.name = 'PLATOON'
    summaryDataFrames.append(platoonCW)

    velocityCW = calcCWS(calculations.velocity, currentIncidentPeriod, previousIncidentPeriod)
    velocityCW.index.name = 'VELOCITY'
    summaryDataFrames.append(velocityCW)

    injMosCW = calcCWS(calculations.injuredMOS, currentInteractionPeriod, previousInteractionPeriod)
    injMosCW.index.name = 'INJURED MOS'
    summaryDataFrames.append(injMosCW)

    triArrestCW = calcCWS(calculations.triArrests, currentIncidentPeriod, previousIncidentPeriod, currentArrestPeriod, previousArrestPeriod)
    triArrestCW.index.name = 'TRIs WITH ARREST'
    summaryDataFrames.append(triArrestCW)

    weaponsCW = calcCWS(calculations.weapons, currentInteractionPeriod, previousInteractionPeriod)
    weaponsCW.index.name = 'FORCE USED BY MOS'
    summaryDataFrames.append(weaponsCW)

    level2CW = calcCWS(calculations.level2, currentIncidentPeriod, previousIncidentPeriod)
    level2CW.index.name = 'LEVEL 2'
    summaryDataFrames.append(level2CW)

    return summaryDataFrames
