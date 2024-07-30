import calculations
from pandas import DataFrame
from pandas import concat

columnOrder = ['PBMS','PBMN','PBBX','PBBS','PBBN','PBQS','PBQN','PBSI','PSB','HB','TB','DB','CSO','OTHER','CityWide']

def calcLevelsCWB(currentIncidentPeriod, currentIncidentYTD):
    periodLevelsPSB,percentPeriodLevelsPSB = calculations.levelsBreakdown(currentIncidentPeriod, 'PSB')
    periodLevelsOTHER, percentPeriodLevelsOTHER = calculations.levelsBreakdown(currentIncidentPeriod, 'OTHER')
    periodLevelsCW, percentPeriodLevelsCW = calculations.levelsBreakdown(currentIncidentPeriod, 'CW')

    periodLevelsALL = concat([periodLevelsPSB, periodLevelsOTHER, periodLevelsCW], axis=1)
    periodLevelsALL = periodLevelsALL[columnOrder]

    percentLevelsALL = concat([percentPeriodLevelsPSB, percentPeriodLevelsOTHER, percentPeriodLevelsCW], axis=1)
    percentLevelsALL = percentLevelsALL[columnOrder]

    ytdLevelsPSB,percentYTDLevelsPSB = calculations.levelsBreakdown(currentIncidentYTD, 'PSB')
    ytdLevelsOTHER, percentYTDLevelsOTHER = calculations.levelsBreakdown(currentIncidentYTD, 'OTHER')
    ytdLevelsCW, percentYTDLevelsCW = calculations.levelsBreakdown(currentIncidentYTD, 'CW')

    ytdLevelsALL = concat([ytdLevelsPSB, ytdLevelsOTHER, ytdLevelsCW], axis=1)
    ytdLevelsALL = ytdLevelsALL[columnOrder]

    percentYTDLevelsALL = concat([percentYTDLevelsPSB, percentYTDLevelsOTHER, percentYTDLevelsCW], axis=1)
    percentYTDLevelsALL = percentYTDLevelsALL[columnOrder]

    return periodLevelsALL, percentLevelsALL, ytdLevelsALL, percentYTDLevelsALL

def calcCWB(func, period, arrestPeriod=None):
    dataPSB : DataFrame
    dataOTHER : DataFrame
    dataCW : DataFrame

    if func == calculations.triArrests:
        dataPSB = func(period, arrestPeriod, 'PSB')
        dataOTHER = func(period, arrestPeriod, 'OTHER')
        dataCW = func(period,arrestPeriod, 'CW')
    else:
        dataPSB = func(period, 'PSB')
        dataOTHER = func(period, 'OTHER')
        dataCW = func(period, 'CW')


    cwIncident = concat([dataPSB,dataOTHER,dataCW], axis=1)
    cwIncident = cwIncident[columnOrder]

    return cwIncident

def periodBreakdown(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentArrestPeriod):
    breakdownDataFrames = []

    periodLevelsCWB, periodPercentLevelsCWB, ytdLevelsCWB, ytdPercentLevelsCWB = calcLevelsCWB(currentIncidentPeriod, currentIncidentYTD)
    periodLevelsCWB.index.name = 'FORCE LEVELS PERIOD' #CHANGE THE INDEX TO CORRESPOND TO THE TABLE TITLE IN THE POWERPOINT
    periodPercentLevelsCWB.index.name = 'FORCE LEVELS PERIOD %'
    ytdLevelsCWB.index.name = 'FORCE LEVELS YTD'
    ytdPercentLevelsCWB.index.name = 'FORCE LEVELS YTD %'
    breakdownDataFrames.extend([periodLevelsCWB, periodPercentLevelsCWB, ytdLevelsCWB, ytdPercentLevelsCWB])

    dowCWB = calcCWB(calculations.dow, currentIncidentPeriod)
    dowCWB.index.name = 'DAYS OF WEEK'
    breakdownDataFrames.append(dowCWB)

    platoonCWB = calcCWB(calculations.platoon,currentIncidentPeriod)
    platoonCWB.index.name = 'PLATOON'
    breakdownDataFrames.append(platoonCWB)

    velocityCWB = calcCWB(calculations.velocity, currentIncidentPeriod)
    velocityCWB.index.name = 'VELOCITY'
    breakdownDataFrames.append(velocityCWB)

    subInjCWB = calcCWB(calculations.subjectInjuryLevels, currentIncidentPeriod)
    subInjCWB.index.name = 'SUBJECT INJURY LEVELS'
    breakdownDataFrames.append(subInjCWB)

    injMosCWB = calcCWB(calculations.injuredMOS, currentInteractionPeriod)
    injMosCWB.index.name = 'INJURED MOS'
    breakdownDataFrames.append(injMosCWB)

    reasonForceCWB = calcCWB(calculations.reasonForce, currentInteractionPeriod)
    reasonForceCWB.index.name = 'REASON FORCE'
    breakdownDataFrames.append(reasonForceCWB)

    triArrestsCWB = calcCWB(calculations.triArrests, currentIncidentPeriod, currentArrestPeriod)
    triArrestsCWB.index.name = 'TRIs WITH ARRESTS'
    breakdownDataFrames.append(triArrestsCWB)

    boeCWB = calcCWB(calculations.boe, currentIncidentPeriod)
    boeCWB.index.name = 'BASIS OF ENCOUNTER'
    breakdownDataFrames.append(boeCWB)

    weaponsCWB = calcCWB(calculations.weapons, currentInteractionPeriod)
    weaponsCWB.index.name = 'TYPE OF PHYSICAL FORCE'
    breakdownDataFrames.append(weaponsCWB)

    return breakdownDataFrames