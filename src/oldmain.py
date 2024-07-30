import sys
import os

from traceback import print_exc

import tkinter as tk
from tkinter import filedialog


from threading import Thread
import subprocess

from datetime import datetime

from dateutil.relativedelta import relativedelta
from tkcalendar import Calendar

# import pandas as pd
from pandas import to_datetime

import read
import clean
import reset
import cwSummary
import cwBreakdown
import output

currentDirectory = os.getcwd()
fileDirectory = os.getcwd()
fileName = 'CityWidePeriodOutput.xlsx'

incallPath : tk.StringVar
intallPath : tk.StringVar
arrestsPath : tk.StringVar

dateStartCurrVar : tk.StringVar
dateEndCurrVar : tk.StringVar
ytdCurrVar : tk.StringVar

dateStartPre = None
dateEndPre = None
ytdPre = None

periodLength = 27

statusText : tk.StringVar
statusLabel : tk.Label

option = 0 # 0 for 28 day timespan, 1 for custom

running = 0

bgColor = '#1a1625'
buttonColor = '#46424f'
textColor = 'white'
entryTextColor = 'black'
entryColor = 'white'
outputTextColor = '#C8C8C8'
outputTextBoxColor = '#121212'
statusGreen = '#4CBC3D'
statusRed = '#BC3D3D'
statusYellow = '#D5DB4E'

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def selectIncallPath(incallPath):
    """
    Opens a file dialog to select an incall path and sets the selected path to the provided incallPath variable.

    Parameters:
    incallPath (tkinter.StringVar): The variable to store the selected incall path.

    Returns:
    None
    """
    global fileDirectory
    incallPath.set(filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(incallPath.get())

def selectIntallPath(intallPath):
    """
    Opens a file dialog to select a file and sets the selected file path to the given `intallPath` variable.

    Parameters:
    intallPath (tkinter.StringVar): The variable to store the selected file path.

    Returns:
    None
    """
    global fileDirectory
    intallPath.set(filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(intallPath.get())

def selectArrestsPath(arrestsPath):
    """
    Opens a file dialog to select a file and sets the selected file path to the `arrestsPath` variable.

    Parameters:
    arrestsPath (tkinter.StringVar): A tkinter variable to store the selected file path.

    Returns:
    None
    """
    global fileDirectory
    arrestsPath.set(filedialog.askopenfilename(initialdir=fileDirectory))
    fileDirectory = os.path.dirname(arrestsPath.get())

def process():
    global running
    global statusText
    global currentDirectory
    global fileName

    global incallPath
    global intallPath
    global arrestsPath

    global dateStartPre
    global dateEndPre
    global ytdPre

    global dateStartCurrVar
    global dateEndCurrVar
    global ytdCurrVar

    if running == 1:
        return

    try:
        running = 1
        statusText.set("Status: Working...")
        statusLabel.config(bg=bgColor, fg=statusYellow)
        print(f"Checking to see if an output file already exists at {currentDirectory}\\{fileName}...\n", file=sys.stdout)

        try:    
            if os.path.exists(f"{currentDirectory}\\{fileName}"):
                os.remove(f"{currentDirectory}\\{fileName}")
                print("Removed old output file.\n")
            else:
                print("File does not exist. Creating new file.\n")
        except PermissionError:
            raise Exception("Output file must be closed to run the program")   
        except Exception as e:
            print(f"Error: {e}\n")
            print_exc()
        
        dateStartCurr = to_datetime(dateStartCurrVar.get())
        dateEndCurr = to_datetime(dateEndCurrVar.get())
        ytdCurr = to_datetime(ytdCurrVar.get())

        if dateStartCurr > dateEndCurr:
            raise Exception("Start must be before End")

        dateStartPre = dateStartCurr - relativedelta(years=1)
        dateEndPre = dateEndCurr - relativedelta(years=1)
        ytdPre = ytdCurr - relativedelta(years=1)

        print('Reading files...', file=sys.stdout)
        incall, intall, arrests = read.readData(incallPath.get(), intallPath.get(), arrestsPath.get())
        print('Done reading.\n', file=sys.stdout)

        print('Cleaning incidents...', file=sys.stdout)
        incall = clean.cleanINCALL(incall)
        print('Cleaned incidents.\n', file=sys.stdout)

        print('Cleaning interactions...', file=sys.stdout)
        intall = clean.cleanINTALL(intall)
        print('Cleaned interactions.\n', file=sys.stdout)

        print('Cleaning arrests...', file=sys.stdout)
        arrests = clean.cleanARRESTS(arrests)
        print('Cleaned arrests.\n', file=sys.stdout)
        
        print('Setting date filters...', file=sys.stdout)

        (currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
        previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
        currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD
        ) = reset.reset(incall,intall,arrests,dateStartCurr,dateEndCurr,dateStartPre,dateEndPre,ytdCurr,ytdPre)

        print('Date filters set.\n', file=sys.stdout)

        print('Building tables...', file=sys.stdout)

        summaryDataFrames = cwSummary.periodSummary(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentInteractionYTD,
        previousIncidentPeriod, previousIncidentYTD, previousInteractionPeriod, previousInteractionYTD,
        currentArrestPeriod, currentArrestYTD, previousArrestPeriod, previousArrestYTD)
        
        breakdownDataFrames = cwBreakdown.periodBreakdown(currentIncidentPeriod, currentIncidentYTD, currentInteractionPeriod, currentArrestPeriod)

        print("Tables built.\n", file=sys.stdout)

        print("Outputting to Excel...", file=sys.stdout)
        output.outputToExcel(summaryDataFrames, breakdownDataFrames, fileName, "CityWide Period Summary", "CityWide Period BreakDown")

        print(f"Output {fileName} at {currentDirectory}.\n", file=sys.stdout)

        subprocess.Popen(f'explorer /select, {currentDirectory}\\{fileName}', shell=True)

        statusText.set("Status: Done. Ready to Start...")
        statusLabel.config(bg=bgColor, fg='green')
        running = 0

    except Exception as e:
        print(f"ERROR: {e}.\n", file=sys.stdout)

        statusText.set("Status: Errored. Make sure inputs are filled out correctly...")
        statusLabel.config(bg=bgColor, fg='red')
        print_exc()
        running = 0

def startProcessing():
    global processThread
    processThread = Thread(target=process)
    processThread.daemon = True
    processThread.start()
    
def pickdate(event,entry,textvar):
    if entry.cget("state") == "disabled":
        return
    
    global cal, dateWindow
    dateWindow = tk.Toplevel()
    dateWindow.grab_set()
    dateWindow.title('Select Date')
    dateWindow.resizable(False, False)
    dateWindow.geometry('250x220+590+370')
    cal = Calendar(dateWindow, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.place(x=0, y=0)

    submitButton = tk.Button(dateWindow, text='Submit', command=lambda: grabDate(entry,textvar))
    submitButton.place(x=80, y=190)

def grabDate(entry,textvar):
    entry.delete(0, tk.END)
    selectedDate = cal.get_date()
    entry.insert(0, selectedDate)
    textvar.set(selectedDate)
    global option
    if option==0:
        dateObject = datetime.strptime(dateEndCurrVar.get(), "%Y-%m-%d")
        startDateFromEnd = dateObject - relativedelta(days=periodLength)
        dateStartCurrVar.set(startDateFromEnd.strftime("%Y-%m-%d"))
    
    ytdCurrVar.set(f"{(dateEndCurrVar.get())[:4]}-01-01") # end date curr var year should change the ytdcurrvar year

    if textvar == dateStartCurrVar:
        print(f"Start Date set to: {textvar.get()}\n",file=sys.stdout)
    elif textvar == dateEndCurrVar:
        print(f"End Date set to: {textvar.get()}\n",file=sys.stdout)
        print(f"YTD set to: {ytdCurrVar.get()}\n",file=sys.stdout)

    dateWindow.destroy()

def toggleEntries():
    global option
    selectedOption = choiceVar.get()
    if selectedOption == "option1":
        option = 0
        startDateEntry.config(state='disabled')
        endDateEntry.config(state='disabled')
        defaultDayEntry.config(state='normal')
    elif selectedOption == "option2":
        option = 1
        startDateEntry.config(state='normal')
        endDateEntry.config(state='normal')
        defaultDayEntry.config(state='disabled')

def main():
    global incallPath
    global intallPath
    global arrestsPath

    global dateStartCurrVar
    global dateEndCurrVar
    global ytdCurrVar

    global bgColor
    global buttonColor
    global textColor
    global entryTextColor
    global entryColor
    global outputTextColor
    global outputTextBoxColor

    root = tk.Tk()
    root.title('CityWide Period Statistics')
    root.geometry('600x500')
    root.config(bg=bgColor)
    # root.iconbitmap(resource_path('nypd.ico'))
    
    root.grid_columnconfigure(0, weight=1)

    incallPath = tk.StringVar(root)
    intallPath = tk.StringVar(root)
    arrestsPath = tk.StringVar(root)

    dateStartCurrVar = tk.StringVar(root)
    dateStartCurrVar.set('< Click to Select >')
    dateEndCurrVar = tk.StringVar(root)
    dateEndCurrVar.set('< Click to Select >')
    ytdCurrVar = tk.StringVar(root)
    ytdCurrVar.set('< Click to Select >')

    incidentFrame = tk.Frame(root)
    incidentFrame.config(bg=bgColor)
    incidentFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    
    tk.Label(incidentFrame, text="Select Incident File:", fg=textColor, bg=bgColor).grid(row=0, column=0)
    tk.Button(incidentFrame, text="< Click To Browse: >", fg=textColor,bg=buttonColor, command=lambda: selectIncallPath(incallPath)).grid(row=1, column=0, sticky="ew")
    tk.Entry(incidentFrame, textvariable=incallPath, state='readonly',readonlybackground=entryColor,borderwidth=0, fg=entryTextColor).grid(row=1, column=1, sticky="ew")
    incidentFrame.grid_columnconfigure(1, weight=1)

    interactionFrame = tk.Frame(root)
    interactionFrame.config(bg=bgColor)
    interactionFrame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    tk.Label(interactionFrame, text="Select Interaction File:",fg=textColor, bg=bgColor).grid(row=0, column=0)
    tk.Button(interactionFrame, text="< Click To Browse: >", fg=textColor,bg=buttonColor, command=lambda: selectIntallPath(intallPath)).grid(row=1, column=0,sticky="ew") 
    tk.Entry(interactionFrame, textvariable=intallPath, state='readonly',readonlybackground=entryColor,borderwidth=0, fg=entryTextColor).grid(row=1, column=1, sticky="ew")
    interactionFrame.grid_columnconfigure(1, weight=1)

    arrestsFrame = tk.Frame(root)
    arrestsFrame.config(bg=bgColor)
    arrestsFrame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    tk.Label(arrestsFrame, text="Select Arrests File:",fg=textColor, bg=bgColor).grid(row=0, column=0)
    tk.Button(arrestsFrame, text="< Click To Browse: >", fg=textColor,bg=buttonColor, command=lambda: selectArrestsPath(arrestsPath)).grid(row=1, column=0, sticky="ew")
    tk.Entry(arrestsFrame, textvariable=arrestsPath, state='readonly',readonlybackground=entryColor,borderwidth=0, fg=entryTextColor).grid(row=1, column=1, sticky="ew")
    arrestsFrame.grid_columnconfigure(1, weight=1)

    global choiceVar,startDateEntry,endDateEntry,defaultDayEntry

    choiceVar = tk.StringVar(value="option1")

    defaultDayFrame = tk.Frame(root)
    defaultDayFrame.config(bg=bgColor)
    defaultDayFrame.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    option2_radio = tk.Radiobutton(defaultDayFrame, text="28 Day Span:", bg=bgColor, fg=textColor, variable=choiceVar, value="option1", selectcolor=bgColor, command=toggleEntries)
    option2_radio.grid(row=3, column=0, sticky="w")

    tk.Label(defaultDayFrame, text="28 Days Before: ", bg=buttonColor, fg=textColor).grid(row=3, column=2)
    defaultDayEntry = tk.Entry(defaultDayFrame, text="28 Days Before:", bg=entryColor, fg=entryTextColor, insertbackground=textColor, textvariable=dateEndCurrVar)
    defaultDayEntry.grid(row=3, column=3, sticky="ew")
    defaultDayEntry.bind('<1>', lambda event: pickdate(event, defaultDayEntry,dateEndCurrVar))
    defaultDayEntry.bind("<Key>", lambda a: "break")

    customDayFrame = tk.Frame(root)
    customDayFrame.config(bg=bgColor)
    customDayFrame.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

    option1Radio = tk.Radiobutton(customDayFrame, text="Custom Timespan:", bg=bgColor, fg=textColor, variable=choiceVar, value="option2", selectcolor=bgColor, command=toggleEntries)
    option1Radio.grid(row=0, column=0, sticky="w")

    
    tk.Label(customDayFrame, text="Start Date", bg=buttonColor, fg=textColor).grid(row=0, column=2)
    startDateEntry = tk.Entry(customDayFrame, text="Start Date", bg=entryColor, fg=entryTextColor, insertbackground=textColor,textvariable=dateStartCurrVar)
    startDateEntry.grid(row=0, column=3, sticky="ew")
    startDateEntry.bind('<1>', lambda event: pickdate(event, startDateEntry,dateStartCurrVar))
    startDateEntry.config(state='disabled')
    startDateEntry.bind("<Key>", lambda a: "break")

    
    tk.Label(customDayFrame, text="End Date", bg=buttonColor, fg=textColor).grid(row=1, column=2)
    endDateEntry = tk.Entry(customDayFrame, text="End Date", bg=entryColor, fg=entryTextColor, insertbackground=textColor, textvariable=dateEndCurrVar)
    endDateEntry.grid(row=1, column=3, sticky="ew")
    endDateEntry.bind('<1>', lambda event: pickdate(event, endDateEntry,dateEndCurrVar))
    endDateEntry.config(state='disabled')
    endDateEntry.bind("<Key>", lambda a: "break")

    processFrame = tk.Frame(root)
    processFrame.config(bg=bgColor)
    processFrame.grid(row=7, column=0, padx=5, pady=5, sticky="ew")
    processFrame.grid_columnconfigure(0, weight=1)

    tk.Button(processFrame, text="Generate CityWide Report", bg=buttonColor, fg=textColor, command=startProcessing).grid(row=0, column=0, pady=5, sticky="ew")


    statusFrame = tk.Frame(root)
    statusFrame.config(bg=bgColor)
    statusFrame.grid(row=8, column=0, padx=5, pady=5, sticky="ew")
    statusFrame.columnconfigure(2, weight=1)

    global statusText
    global statusLabel

    statusText = tk.StringVar()
    statusText.set("Status: Ready to Start")
    statusLabel = tk.Label(statusFrame, textvariable=statusText, bg=bgColor, fg=textColor)
    statusLabel.config(bg=bgColor, fg=statusGreen)
    statusLabel.grid(row=0, column=0, sticky="nsew")

    root.grid_rowconfigure(9, weight=1)
    outputFrame = tk.Frame(root)
    outputFrame.config(bg=bgColor)
    outputFrame.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
    outputFrame.grid_rowconfigure(0, weight=1)
    outputFrame.grid_columnconfigure(0, weight=1)

    outputTextBox = tk.Text(outputFrame, height=5, width=50, bg=outputTextBoxColor, fg=outputTextColor,font=('Calibri', 10), wrap='word')
    outputTextBox.grid(row=0, column=0, sticky="nsew")

    def outputRedirector(inputStr):
        outputTextBox.insert(tk.END,inputStr)
        outputTextBox.see(tk.END)

    sys.stdout.write = outputRedirector # whenever sys.stdout.write is called, redirector is called.

    root.mainloop()

if __name__ == "__main__":
    main()
