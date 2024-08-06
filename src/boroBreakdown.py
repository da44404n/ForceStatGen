from pandas import DataFrame, concat
import calculations

boroDict = {

            'PBBN' : { '073','075','077',
                       '079','080','081','082','083',
                       '084','085','086','087','088',
                       '089','090','091','092','093',
                       '094','164','186'
                        },
            'PBBS' : { '060','061','062','063','064',
                       '065','066','067','068','069',
                       '69','070','071','072','076',
                       '078','164','186'
                        },
            'PBMN' : { '019','020','022','023','024',
                       '025','026','028','28','030','032',
                       '033','034','162','182','483' 
                        },
            'PBMS' : { '001','002','003','004','005','006',
                       '007','008','009','010','011','012',
                       '013','014','015','016','017','018',
                       '161','181'
                        },
            'PBQS' : {  '100','101','102','103','105','106',
                        '107', '113','171','185'
                        },
            'PBQN' : {  '104','108','109','110','111','112',
                        '114','115','169','184'
                        },
            'PBBX' : {  '040','041','042','043','044','045',
                        '046','047','048','049','050','051',
                        '052', '163','183'
                        },
            'PBSI' : {  '120','121','122','123','437','447'
                        },
            'HB' : {  '800','801','801','802','803','804',
                      '805','806','807','808','809','810',
                      '820','821','821','822','823','824',
                      '825','826','827','828','829','830',
                      '831','832','833','834','835'
                        },
            'TB' : { '840','848','849','849','850','851','852',
                    '853','854','855','856','857','858','859',
                    '860','861','862','863','864','865','866',
                    '867','868','869','870','871','872','873',
                    '874','875','876','877','878','879','880'
                        },
}

def calcLevelsBBD(boro, period):
    pctList = list(boroDict[boro])

    pctCols = period[['OWNING COMMAND','OWNING_COMMAND_CODE']]
    pctDict = pctCols.set_index('OWNING_COMMAND_CODE')['OWNING COMMAND'].to_dict()
    pctDict = {key.lstrip('0'): value for key, value in pctDict.items()}

    boroLevel, boroLevelP = calculations.levelsBreakdown(period, 'OWNING_COMMAND_CODE')
    boroLevel.columns = [col.lstrip('0') for col in boroLevel.columns]
    boroLevelP.columns = [col.lstrip('0') for col in boroLevelP.columns]

    presentPcts = [col.lstrip('0') for col in pctList if int(col) in boroLevel.columns.astype(int)]
    presentPcts.sort()
    
    try:
        boroLevel = boroLevel[presentPcts]
        boroLevelP = boroLevelP[presentPcts]

        boroLevel.columns = boroLevel.columns.map(pctDict)
        boroLevelP.columns = boroLevelP.columns.map(pctDict)
    except:
        boroLevel = DataFrame()
        boroLevelP = DataFrame()

    boroTotal, boroTotalP = calculations.levelsBreakdown(period, 'ALLBORO')

    boroTotal = boroTotal[boro]
    boroLevel = boroLevel.join(boroTotal)

    boroTotalP = boroTotalP[boro]
    boroLevelP = boroLevelP.join(boroTotalP)

    boroLevelCW, boroLevelCWP = calculations.levelsBreakdown(period, 'CW')

    boroBreakdown = boroLevel.join(boroLevelCW)
    boroBreakdownPercent = boroLevelP.join(boroLevelCWP)
    return boroBreakdown, boroBreakdownPercent

def calcIncBBD(func, boro, period):
    pctList = list(boroDict[boro])

    pctCols = period[['OWNING COMMAND','OWNING_COMMAND_CODE']]
    pctDict = pctCols.set_index('OWNING_COMMAND_CODE')['OWNING COMMAND'].to_dict()
    pctDict = {key.lstrip('0'): value for key, value in pctDict.items()}

    boroInc = func(period, 'OWNING_COMMAND_CODE')
    boroInc.columns = [col.lstrip('0') for col in boroInc.columns]

    presentPcts = [col.lstrip('0') for col in pctList if int(col) in boroInc.columns.astype(int)]

    presentPcts.sort()

    try:
        boroInc = boroInc[presentPcts]
        boroInc.columns = boroInc.columns.map(pctDict)
    except:
        boroInc = DataFrame()

    boroTotal = func(period, 'ALLBORO')

    boroTotal = boroTotal[boro]
    boroInc = boroInc.join(boroTotal)

    boroIncCW = func(period, 'CW')

    boroBreakdown = boroInc.join(boroIncCW)
    return boroBreakdown

def calcIntBBD(func, boro, period):    
    pctList = list(boroDict[boro])

    pctCols = period[['MOS Command Description','MOS Command Code']]
    pctDict = pctCols.set_index('MOS Command Code')['MOS Command Description'].to_dict()
    pctDict = {key.lstrip('0'): value for key, value in pctDict.items()}
    pctDict = {key.rstrip(' '): value for key, value in pctDict.items()}

    boroInt = func(period, 'MOS Command Code')
    boroInt.columns = [col.lstrip('0') for col in boroInt.columns]
    boroInt.columns = [col.rstrip(' ') for col in boroInt.columns]

    presentPcts = [col.lstrip('0') for col in pctList if int(col) in boroInt.columns.astype(int)]

    presentPcts.sort()

    try:
        boroInt = boroInt[presentPcts]
        boroInt.columns = boroInt.columns.map(pctDict)
    except:
        boroInt = DataFrame()

    boroTotal = func(period, 'ALLBORO')

    boroTotal = boroTotal[boro]
    boroInt = boroInt.join(boroTotal)

    boroIntCW = func(period, 'CW')

    boroBreakdown = boroInt.join(boroIntCW)
    return boroBreakdown

def triCalc(incidentperiod, incGroup):
    if incidentperiod.empty:
        return DataFrame()

    thisPeriod = incidentperiod.groupby(by=incGroup, observed=False).agg(
        TRICount=('IncidentCount', 'sum'),
        TRIwArrest=('Arrest Made Flag', 'sum'),
        ArrestForce=('ArrFor', 'sum')
    )

    thisPeriod.columns = ['Total TRIs', 'TRIs w/ Arrests', 'TRIs w/ Arrests where MOS used force']

    thisPeriod = thisPeriod.T
    return thisPeriod

def arrestsCalc(arrestPeriod, arrGroup):
    if arrestPeriod.empty:
        return DataFrame()
    
    thisPeriod = arrestPeriod.groupby(by=arrGroup, observed=False).agg(
        Arrests = ('ArrestCount', 'sum')
    )

    thisPeriod = thisPeriod.T
    return thisPeriod

def calcTriArrestsBBD(boro, incidentPeriod, arrestPeriod):
    global boroTRI
    global boroArrests
    global boroTriArrestTotal

    pctList = list(boroDict[boro])

    pctCols = incidentPeriod[['OWNING COMMAND','OWNING_COMMAND_CODE']]
    pctDict = pctCols.set_index('OWNING_COMMAND_CODE')['OWNING COMMAND'].to_dict()
    pctDict = {key.lstrip('0'): value for key, value in pctDict.items()}

    boroTRI = triCalc(incidentPeriod, 'OWNING_COMMAND_CODE')
    boroTRI.columns = [col.lstrip('0') for col in boroTRI.columns]

    arrestPeriod['Arresting_MOS_Command_Code'] = arrestPeriod['Arresting_MOS_Command_Code'].astype(str)

    boroArrests = arrestsCalc(arrestPeriod, 'Arresting_MOS_Command_Code')
    boroArrests.columns = [col.lstrip('0') for col in boroArrests.columns]

    boroTriArrests = concat([boroTRI, boroArrests])
    boroTriArrests = boroTriArrests.T

    # boroTriArrests['% of Total Arrests'] = (boroTriArrests['TRIs w/ Arrests where MOS used force'].dropna().astype(int) / boroTriArrests['Arrests'].dropna().astype(int)).apply(lambda x: f"{x:.0%}")
    boroTriArrests['% of Total Arrests'] = (boroTriArrests['TRIs w/ Arrests where MOS used force'].apply(calculations.fstringToInt) / boroTriArrests['Arrests'].apply(calculations.fstringToInt)).apply(lambda x: f"{x:.0%}")
    
    boroTriArrests = boroTriArrests.T

    presentPcts = [col.lstrip('0') for col in pctList if int(col) in boroTRI.columns.astype(int)]
    presentPcts.sort()

    try:
        boroTriArrests = boroTriArrests[presentPcts].fillna(0)
        boroTriArrests.columns = boroTriArrests.columns.map(pctDict)
    except:
        boroTriArrests = DataFrame()

    boroTriTotal = triCalc(incidentPeriod, 'ALLBORO')

    boroArrestTotal = arrestsCalc(arrestPeriod, 'ALLBORO')

    boroTriArrestTotal = concat([boroTriTotal.T, boroArrestTotal.T], axis=1)

    boroTriArrestTotal['% of Total Arrests'] = (boroTriArrestTotal['TRIs w/ Arrests where MOS used force'] / boroTriArrestTotal['Arrests']).apply(lambda x: f"{x:.0%}")

    boroTriArrestTotal = boroTriArrestTotal.T

    boroTriArrestTotal = boroTriArrestTotal[boro]

    boroTriArrestTotal = boroTriArrestTotal.T

    boroTriCW = triCalc(incidentPeriod, 'CW')
    boroArrestCW = arrestsCalc(arrestPeriod, 'CW')

    boroTriArrestCW = concat([boroTriCW,boroArrestCW])
    boroTriArrestCW = boroTriArrestCW.T

    boroTriArrestCW['% of Total Arrests'] = (boroTriArrestCW['TRIs w/ Arrests where MOS used force']) / (boroTriArrestCW['Arrests'])
    boroTriArrestCW['% of Total Arrests'] = boroTriArrestCW['% of Total Arrests'].apply(lambda x: f"{x:.0%}")
    boroTriArrestCW = boroTriArrestCW.T

    boroTriArrestsBreakdown = concat([boroTriArrests, boroTriArrestTotal, boroTriArrestCW], axis=1)

    return boroTriArrestsBreakdown

def boroBreakdown(boro, currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentArrestPeriod):
    breakdownDataFrames = []

    periodLevelsBBD, periodLevelsPercentBBD = calcLevelsBBD(boro, currentIncidentPeriod)
    periodLevelsBBD.index.name = 'FORCE LEVELS PERIOD' #CHANGE THE INDEX TO CORRESPOND TO THE TABLE TITLE IN THE POWERPOINT
    periodLevelsPercentBBD.index.name = 'FORCE LEVELS PERIOD %'
    breakdownDataFrames.extend([periodLevelsBBD, periodLevelsPercentBBD])

    ytdLevelsBBD, ytdLevelsPercentBBD = calcLevelsBBD(boro, currentIncidentYTD)
    ytdLevelsBBD.index.name = 'FORCE LEVELS YTD'
    ytdLevelsPercentBBD.index.name = 'FORCE LEVELS YTD %'
    breakdownDataFrames.extend([ytdLevelsBBD, ytdLevelsPercentBBD])

    dowBBD = calcIncBBD(calculations.dow, boro, currentIncidentPeriod)
    dowBBD.index.name = 'DAYS OF WEEK'
    breakdownDataFrames.append(dowBBD)

    platoonBBD = calcIncBBD(calculations.platoon, boro, currentIncidentPeriod)
    platoonBBD.index.name = 'PLATOON'
    breakdownDataFrames.append(platoonBBD)

    velocityBBD = calcIncBBD(calculations.velocity, boro, currentIncidentPeriod)
    velocityBBD.index.name = 'VELOCITY'
    breakdownDataFrames.append(velocityBBD)

    subInjBBD = calcIncBBD(calculations.subjectInjuryLevels, boro, currentIncidentPeriod)
    subInjBBD.index.name = 'SUBJECT INJURY LEVELS'
    breakdownDataFrames.append(subInjBBD)

    injMosBBD = calcIntBBD(calculations.injuredMOS, boro, currentInteractionPeriod)
    injMosBBD.index.name = 'INJURED MOS'
    breakdownDataFrames.append(injMosBBD)

    reasonForceBBD = calcIntBBD(calculations.reasonForce, boro, currentInteractionPeriod)
    reasonForceBBD.index.name = 'REASON FORCE'
    breakdownDataFrames.append(reasonForceBBD)

    triArrestsBBD = calcTriArrestsBBD(boro, currentIncidentPeriod, currentArrestPeriod)
    triArrestsBBD.index.name = 'TRIs WITH ARRESTS'
    breakdownDataFrames.append(triArrestsBBD)

    boeBBD = calcIncBBD(calculations.boe, boro, currentIncidentPeriod)
    boeBBD.index.name = 'BASIS OF ENCOUNTER'
    breakdownDataFrames.append(boeBBD)

    weaponsBBD = calcIntBBD(calculations.weapons, boro, currentInteractionPeriod)
    weaponsBBD.index.name = 'TYPE OF PHYSICAL FORCE'
    breakdownDataFrames.append(weaponsBBD)

    return breakdownDataFrames