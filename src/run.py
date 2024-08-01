import os

from traceback import format_exc

import subprocess

from pandas import to_datetime
from pandas import DataFrame

from dateutil.relativedelta import relativedelta

import read
import clean
import filter
import cwSummary
import cwBreakdown
import overviewPpt
import boroSummary
import boroBreakdown
import output

def process(templatePath, outputDirectory, reportPath, presentationPath, incallPath, intallPath, arrestsPath, dateStart, dateEnd, ytd, cw, boroList, queue):
    try:
        queue.put("Removing old output files...")

        if not os.path.exists(templatePath):
            queue.put("Missing PowerPoint template file. Skipping that step...")

        if not os.path.exists(outputDirectory):
            os.mkdir(outputDirectory)

        if os.path.exists(reportPath):
            os.remove(reportPath)
            queue.put("Removed old report spreadsheet.")
        else:
            queue.put("Report does not exist. Creating new one.")

        if os.path.exists(presentationPath):
            os.remove(presentationPath)
            queue.put("Removed old overview presentation.")
        else:
            queue.put("Presentation does not exist. Creating new one.")

        if dateStart.startswith('<') or dateEnd.startswith('<') or ytd.startswith('<'):
            raise Exception("Please select a date range.")

        if not cw and not boroList:
            raise Exception("Please select CityWide or a borough.")

        dateStartCurr = to_datetime(dateStart)
        dateEndCurr = to_datetime(dateEnd)
        ytdCurr = to_datetime(ytd)

        dateStartPre = dateStartCurr - relativedelta(years=1)
        dateEndPre = dateEndCurr - relativedelta(years=1)
        ytdPre = ytdCurr - relativedelta(years=1)

        queue.put('Reading files...')
        incall, intall, arrests = read.readData(incallPath, intallPath, arrestsPath)
        queue.put('Done reading.')

        queue.put('Cleaning incidents...')
        incall = clean.cleanINCALL(incall)
        queue.put('Cleaned incidents.')

        queue.put('Cleaning interactions...')
        intall = clean.cleanINTALL(intall)
        queue.put('Cleaned interactions.')

        queue.put('Cleaning arrests...')
        arrests = clean.cleanARRESTS(arrests)
        queue.put('Cleaned arrests.')

        queue.put('Setting date filters...')

        (currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
        previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
        currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD
        ) = filter.dates(incall,intall,arrests,dateStartCurr,dateEndCurr,dateStartPre,dateEndPre,ytdCurr,ytdPre)

        queue.put('Date filters set.')

        dateDict = { 'Date Start:' : [dateStartCurr.strftime('%m/%d/%Y')], 'Date End:' : [dateEndCurr.strftime('%m/%d/%Y')]}
        dateDataFrame = DataFrame(dateDict)
        dateDataFrame.index = ['Date:']

        cwTablesDict = {}

        if cw == True:
            queue.put('Building CityWide tables...')

            summaryDataFrames = cwSummary.periodSummary(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
            previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
            currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD)

            breakdownDataFrames = cwBreakdown.periodBreakdown(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentArrestPeriod)

            summaryDataFrames = [dateDataFrame] + summaryDataFrames
            breakdownDataFrames = [dateDataFrame] + breakdownDataFrames

            cwTablesDict["CityWide Period Summary"] = summaryDataFrames
            cwTablesDict["CityWide Period Breakdown"] = breakdownDataFrames

            queue.put("CityWide tables built.")

        boroTablesDict = {}

        for boro in boroList:
            queue.put('Building borough tables...')

            summaryBoroDataFrames = boroSummary.boroSummary(boro, currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
                            previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
                            currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD)
            
            breakdownBoroDataFrames = boroBreakdown.boroBreakdown(boro, currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentArrestPeriod)

            summaryBoroDataFrames = [dateDataFrame] + summaryBoroDataFrames
            breakdownBoroDataFrames = [dateDataFrame] + breakdownBoroDataFrames

            boroTablesDict[f"{boro} Summmary"] = summaryBoroDataFrames
            boroTablesDict[f"{boro} Breakdown"] = breakdownBoroDataFrames

            queue.put("Borough tables built.")

        outputDict = cwTablesDict | boroTablesDict

        queue.put("Outputting to Excel...")

        output.outputToExcel(outputDict, reportPath)

        queue.put(f"Output excel sheet to {reportPath}")

        if cw==True and os.path.exists(templatePath):
            queue.put("Filling overview presentation...")

            overviewPpt.fillPresentation(templatePath, presentationPath, summaryDataFrames, breakdownDataFrames, dateStartCurr, dateEndCurr)

            queue.put(f"Output presentation to {presentationPath}")

        queue.put("Done.")

        subprocess.Popen(f'explorer /select, {reportPath}', shell=True)
    
    except PermissionError:
        queue.put("ERROR: Output files must be closed to run the program.")

    except Exception as e:
        error_message = format_exc()

        queue.put(error_message)
        queue.put(f"ERROR: {e}")
