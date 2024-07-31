import os
import sys

from traceback import format_exc

from threading import Thread
import subprocess
import multiprocessing
import time

from datetime import datetime

from pandas import to_datetime
from pandas import DataFrame

from dateutil.relativedelta import relativedelta

import customtkinter as ctk
from tkcalendar import Calendar

import filter
import clean
import reset
import cwSummary
import cwBreakdown
import overviewPpt
import boroSummary
import boroBreakdown
import output

if getattr(sys, 'frozen', False):
    import pyi_splash

# ctk.set_appearance_mode("System")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
DISABLEDCOLOR = 'gray'
ENABLEDCOLOR = 'white'

currentDirectory = os.getcwd()
fileDirectory = currentDirectory
outputDirectory = f'{currentDirectory}\\output'
templateDirectory = f'{currentDirectory}\\template'

# Modify this to change the output file name.
REPORTNAME = 'Force Stat Report'
PRESENTATIONNAME = 'Overview'
TEMPLATENAME = 'Template'

reportPath = f'{outputDirectory}\\{REPORTNAME}.xlsx'
presentationPath = f'{outputDirectory}\\{PRESENTATIONNAME}.pptx'
templatePath = f'{templateDirectory}\\{TEMPLATENAME}.pptx'

PERIODLENGTH = 27

runningBV : ctk.BooleanVar

progressBar : ctk.CTkProgressBar

incall = None

intall = None

arrests = None

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def selectIncallPath(incallPath):
    global fileDirectory
    incallPath.set(ctk.filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(incallPath.get())

def selectIntallPath(intallPath):
    global fileDirectory
    intallPath.set(ctk.filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(intallPath.get())

def selectArrestsPath(arrestsPath):
    global fileDirectory
    arrestsPath.set(ctk.filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(arrestsPath.get())

def toggleEntries(optionSV, defaultSpanEntry, customStartEntry, customEndEntry):
    if optionSV.get() == 'option1':
        defaultSpanEntry.configure(state='normal', text_color=ENABLEDCOLOR)

        customStartEntry.configure(state='disabled', text_color=DISABLEDCOLOR)
        customEndEntry.configure(state='disabled', text_color=DISABLEDCOLOR)

    elif optionSV.get() == 'option2':
        defaultSpanEntry.configure(state='disabled', text_color=DISABLEDCOLOR)

        customStartEntry.configure(state='normal', text_color=ENABLEDCOLOR)
        customEndEntry.configure(state='normal', text_color=ENABLEDCOLOR)

def grabDate(dateWindow, entry, calendar, optionSV, changeSV, dateStartSV, dateEndSV, ytdSV):
    entry.delete(0,ctk.END)
    selectedDate = calendar.get_date()
    entry.insert(0, selectedDate)
    changeSV.set(selectedDate)

    if optionSV.get() == 'option1':
        dateEnd = datetime.strptime(changeSV.get(), "%Y-%m-%d")
        relativeStartDate = dateEnd - relativedelta(days = PERIODLENGTH)
        reltaiveStartDateString = relativeStartDate.strftime("%Y-%m-%d")
        dateStartSV.set(reltaiveStartDateString)

    ytdSV.set(f"{(dateEndSV.get())[:4]}-01-01")

    dateWindow.destroy()

def pickdate(event, entry, optionSV, changeSV, dateStartSV, dateEndSV, ytdSV):
    if entry.cget("state") == "disabled":
        return
    
    dateWindow = ctk.CTkToplevel()
    dateWindow.grab_set()
    dateWindow.title('Select Date')
    dateWindow.resizable(False, False)
    dateWindow.geometry('390x330')

    dateWindow.grid_rowconfigure(0,weight=1)
    dateWindow.grid_columnconfigure(0,weight=1)

    
    calendarFrame = ctk.CTkFrame(dateWindow)
    calendarFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    cal = Calendar(calendarFrame, selectmode='day', date_pattern='yyyy-mm-dd', font='Arial 15 bold', )
    cal.pack(fill='both', expand=True)

    submitButton = ctk.CTkButton(dateWindow, text='Submit', command=lambda:
        grabDate(dateWindow=dateWindow, entry=entry, calendar=cal, optionSV=optionSV, changeSV=changeSV, dateStartSV=dateStartSV, dateEndSV=dateEndSV, ytdSV=ytdSV))
    
    submitButton.grid(row=1,column=0, padx=5, pady=5, sticky="ew")

def selectBoro(boroList, boro):
    if boro in boroList:
        boroList.remove(boro)
    else:
        boroList.append(boro)
    
def process(incallPath, intallPath, arrestsPath, dateStart, dateEnd, ytd, cw, boroList, queue):
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
        incall, intall, arrests = filter.readData(incallPath, intallPath, arrestsPath)
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
        ) = reset.reset(incall,intall,arrests,dateStartCurr,dateEndCurr,dateStartPre,dateEndPre,ytdCurr,ytdPre)

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

def startProcess(runningBV, consoleTextBox, incallPath, intallPath, arrestsPath, dateStart, dateEnd, ytd, cw, boroList):
    if runningBV.get() == True:
        return
    
    runningBV.set(True)
    consoleTextBox.delete('0.0', 'end')
    progressBar.start()
    queue = multiprocessing.Queue()
    statProcess = multiprocessing.Process(target=process, args=(incallPath, intallPath, arrestsPath, dateStart, dateEnd, ytd, cw, boroList, queue))
    statProcess.daemon = True
    
    statProcess.start()

    def monitor_process():
        while statProcess.is_alive() or not queue.empty():
            while not queue.empty():
                message = queue.get() + '\n\n'
                # print(message, file=sys.stdout, flush=True)
                consoleTextBox.insert(ctk.END, message)
                consoleTextBox.see(ctk.END)

            time.sleep(1)  # Adjust the sleep time as necessary
        runningBV.set(False)
        progressBar.stop()

    monitor_thread = Thread(target=monitor_process)
    monitor_thread.daemon = True
    monitor_thread.start()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        multiprocessing.freeze_support()

        try:
            if getattr(sys, 'frozen', False):
                pyi_splash.close()
        except:
            pass

        self.title("ForceStatGen")
        self.geometry("900x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        if getattr(sys, 'frozen', False):
            self.iconbitmap(resource_path('nypd.ico'))


        incallPathSV = ctk.StringVar(self)
        intallPathSV = ctk.StringVar(self)
        arrestsPathSV = ctk.StringVar(self)

        dateStartSV = ctk.StringVar(self, '< Click to Select Start >')
        dateEndSV = ctk.StringVar(self, '< Click to Select End >')
        ytdSV = ctk.StringVar(self)

        optionSV = ctk.StringVar(self, "option1")

        cwBV = ctk.BooleanVar(self, True)
        boroList = []
        global runningBV
        runningBV = ctk.BooleanVar(self, False)


        self.topWidgets(0,0)
        self.fileWidgets(1, 0, incallPathSV, intallPathSV, arrestsPathSV)
        self.spanWidgets(2, 0, optionSV, dateStartSV, dateEndSV, ytdSV)
        self.cwBoroWidgets(3, 0, cwBV, boroList)
        self.progressWidget(5,0)
        consoleTextBox = self.consoleWidget(6,0)
        self.startWidget(4, 0, runningBV, consoleTextBox, incallPathSV, intallPathSV, arrestsPathSV, dateStartSV, dateEndSV, ytdSV, cwBV, boroList)

    def topWidgets(self, row, col):
        topTextFrame = ctk.CTkFrame(self)
        topTextFrame.pack()
        ctk.CTkLabel(topTextFrame, text='Click the buttons below to select data:').pack(padx=5, pady=5, side = ctk.LEFT)
        ctk.CTkLabel(topTextFrame, text='(.csv files are faster than .xlsx files!)').pack(padx=5, pady=5, side = ctk.RIGHT)
        topTextFrame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

    def fileWidgets(self, row, col, incallPathSV, intallPathSV, arrestsPathSV):
        filePathFrame = ctk.CTkFrame(self)
        filePathFrame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        filePathFrame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(filePathFrame, text="Select Incident File:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkButton(filePathFrame, text='< Click To Browse: >', font=('Arial', 13, 'bold'), command=lambda: selectIncallPath(incallPathSV)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(filePathFrame, textvariable=incallPathSV, state='readonly').grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(filePathFrame, text="Select Interaction File:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkButton(filePathFrame, text='< Click To Browse: >', font=('Arial', 13, 'bold'), command=lambda: selectIntallPath(intallPathSV)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(filePathFrame, textvariable=intallPathSV, state='readonly').grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(filePathFrame, text="Select Arrests File:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkButton(filePathFrame, text='< Click To Browse: >', font=('Arial', 13, 'bold'), command=lambda: selectArrestsPath(arrestsPathSV)).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(filePathFrame, textvariable=arrestsPathSV, state='readonly').grid(row=6, column=1, padx=5, pady=5, sticky="ew")

    def spanWidgets(self, row, col, optionSV, dateStartSV, dateEndSV, ytdSV):
        spanFrame = ctk.CTkFrame(self)
        spanFrame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        defaultSpanEntry = ctk.CTkEntry(spanFrame, state='normal', textvariable=dateEndSV, text_color=ENABLEDCOLOR, width=140)
        defaultSpanEntry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        defaultSpanEntry.bind('<1>', lambda event: 
            pickdate(event=event, entry=defaultSpanEntry, optionSV=optionSV, changeSV=dateEndSV, dateStartSV=dateStartSV, dateEndSV=dateEndSV, ytdSV=ytdSV))
        defaultSpanEntry.bind("<Key>", lambda a: "break")

        customStartEntry = ctk.CTkEntry(spanFrame, state='disabled', textvariable=dateStartSV, text_color=DISABLEDCOLOR, width=145)
        customStartEntry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        customStartEntry.bind('<1>', lambda event: 
            pickdate(event=event, entry=customStartEntry, optionSV=optionSV, changeSV=dateStartSV, dateStartSV=dateStartSV, dateEndSV=dateEndSV, ytdSV=ytdSV))
        customStartEntry.bind("<Key>", lambda a: "break")

        toLabel = ctk.CTkLabel(spanFrame,text='and')
        toLabel.grid(row=1,column=2,padx=5, pady=5, sticky="w")

        customEndEntry = ctk.CTkEntry(spanFrame, state='disabled', textvariable=dateEndSV, text_color=DISABLEDCOLOR, width=140)
        customEndEntry.configure(state='disabled')
        customEndEntry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        customEndEntry.bind('<1>', lambda event: 
            pickdate(event=event, entry=customEndEntry, optionSV=optionSV, changeSV=dateEndSV, dateStartSV=dateStartSV, dateEndSV=dateEndSV, ytdSV=ytdSV))
        customEndEntry.bind("<Key>", lambda a: "break")

        defaultSpanRadio = ctk.CTkRadioButton(spanFrame, text="28 Days Before:", variable=optionSV, value="option1", command=lambda: toggleEntries(optionSV, defaultSpanEntry, customStartEntry, customEndEntry))
        defaultSpanRadio.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        defaultSpanRadio.invoke(lambda: toggleEntries(optionSV, defaultSpanEntry, customStartEntry, customEndEntry))

        customSpanRadio = ctk.CTkRadioButton(spanFrame, text="Custom Timespan Between:", variable=optionSV, value="option2", command=lambda: toggleEntries(optionSV, defaultSpanEntry, customStartEntry, customEndEntry))
        customSpanRadio.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def cwBoroWidgets(self, row, col, cwBV, boroList):
        boroFrame = ctk.CTkFrame(self)
        boroFrame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        cwCheck = ctk.CTkCheckBox(boroFrame, text='CityWide', variable=cwBV)
        cwCheck.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        allBoros = ['PBBN', 'PBBS', 'PBMN', 'PBMS', 'PBQN', 'PBQS', 'PBBX', 'PBSI', 'HB', 'TB']

        pbbnCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[0], command=lambda: selectBoro(boroList, allBoros[0]))
        pbbnCheck.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        pbbsCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[1], command=lambda: selectBoro(boroList, allBoros[1]))
        pbbsCheck.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        pbmnCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[2], command=lambda: selectBoro(boroList, allBoros[2]))
        pbmnCheck.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        pbmsCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[3], command=lambda: selectBoro(boroList, allBoros[3]))
        pbmsCheck.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        pbqnCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[4], command=lambda: selectBoro(boroList, allBoros[4]))
        pbqnCheck.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        pbqsCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[5], command=lambda: selectBoro(boroList, allBoros[5]))
        pbqsCheck.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        pbbxCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[6], command=lambda: selectBoro(boroList, allBoros[6]))
        pbbxCheck.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        pbsiCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[7], command=lambda: selectBoro(boroList, allBoros[7]))
        pbsiCheck.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        hbCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[8], command=lambda: selectBoro(boroList, allBoros[8]))
        hbCheck.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        tbCheck = ctk.CTkCheckBox(boroFrame, text=allBoros[9], command=lambda: selectBoro(boroList, allBoros[9]))
        tbCheck.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    def startWidget(self, row, col, runningBV, consoleTextBox, incallPathSV, intallPathSV, arrestsPathSV, dateStartSV, dateEndSV, ytdSV, cwBV, boroList):
        buttonFrame = ctk.CTkFrame(self)
        buttonFrame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        buttonFrame.grid_columnconfigure(0,weight=1)

        startButton = ctk.CTkButton(buttonFrame, text='Generate Report', font=('Arial',13,'bold'), command=lambda: startProcess(runningBV, consoleTextBox, incallPathSV.get(), intallPathSV.get(), arrestsPathSV.get(), dateStartSV.get(), dateEndSV.get(), ytdSV.get(), cwBV.get(), boroList))
        startButton.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def progressWidget(self, row, col):
        global progressBar
        progressFrame = ctk.CTkFrame(self)
        progressFrame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

        # progressLabel = ctk.CTkLabel(progressFrame, text='Progress:')
        # progressLabel.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        progressFrame.grid_columnconfigure(1,weight=1)
        progressBar = ctk.CTkProgressBar(progressFrame, progress_color='#1aaa5a', mode='indeterminate')
        progressBar.set(0)  
        progressBar.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    def consoleWidget(self, row, col):
        outputFrame = ctk.CTkFrame(self)
        outputFrame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        outputFrame.grid_rowconfigure(0,weight=1)
        outputFrame.grid_columnconfigure(0, weight=1)

        outputTextBox = ctk.CTkTextbox(outputFrame, text_color=DISABLEDCOLOR, fg_color='#121212', wrap='word')
        outputTextBox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        outputTextBox.bind("<Key>", lambda a: "break")

        return outputTextBox
    
if __name__ == "__main__":
    app = App()

    app.mainloop()