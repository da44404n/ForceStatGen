# ForceStatGen

## Overview

ForceStatGen is a Python-based application designed to automate the generation of force statistics reports and presentations for the NYPD. The application processes data from various sources, cleans it, and compiles it into comprehensive Excel reports and PowerPoint presentations.

## Features

* **Automated Data Processing** : Reads, cleans, and processes incident, interaction, and arrest data.
* **Customizable Date Ranges** : Allows users to select specific date ranges for the reports.
* **CityWide and Borough Reports** : Generates both citywide and individual borough statistics.
* **Excel and PowerPoint Outputs** : Outputs the results into an Excel file and, if a template is available, a PowerPoint presentation.

## Requirements

* Python 3.x
* Required Python libraries:

  ```
  altgraph==0.17.4
  Babel==2.15.0
  customtkinter==5.2.2
  darkdetect==0.8.0
  et-xmlfile==1.1.0
  lxml==5.2.2
  numpy==2.0.1
  openpyxl==3.1.5
  packaging==24.1
  pandas==2.2.2
  pefile==2023.2.7
  pillow==10.4.0
  pyinstaller==6.9.0
  pyinstaller-hooks-contrib==2024.7
  python-dateutil==2.9.0.post0
  python-pptx==0.6.23
  pytz==2024.1
  pywin32-ctypes==0.2.2
  six==1.16.0
  tkcalendar==1.6.1
  tzdata==2024.1
  xlsx2csv==0.8.3
  XlsxWriter==3.2.0


  ```
* Required Python libraries with Jupyter support:

  ```
  altgraph==0.17.4
  asttokens==2.4.1
  Babel==2.15.0
  colorama==0.4.6
  comm==0.2.2
  customtkinter==5.2.2
  darkdetect==0.8.0
  debugpy==1.8.2
  decorator==5.1.1
  et-xmlfile==1.1.0
  executing==2.0.1
  ipykernel==6.29.5
  ipython==8.26.0
  jedi==0.19.1
  jupyter_client==8.6.2
  jupyter_core==5.7.2
  lxml==5.2.2
  matplotlib-inline==0.1.7
  nest-asyncio==1.6.0
  numpy==2.0.1
  openpyxl==3.1.5
  packaging==24.1
  pandas==2.2.2
  parso==0.8.4
  pefile==2023.2.7
  pillow==10.4.0
  platformdirs==4.2.2
  prompt_toolkit==3.0.47
  psutil==6.0.0
  pure_eval==0.2.3
  Pygments==2.18.0
  pyinstaller==6.9.0
  pyinstaller-hooks-contrib==2024.7
  python-dateutil==2.9.0.post0
  python-pptx==0.6.23
  pytz==2024.1
  pywin32==306
  pywin32-ctypes==0.2.2
  pyzmq==26.0.3
  six==1.16.0
  stack-data==0.6.3
  tkcalendar==1.6.1
  tornado==6.4.1
  traitlets==5.14.3
  typing_extensions==4.12.2
  tzdata==2024.1
  wcwidth==0.2.13
  xlsx2csv==0.8.3
  XlsxWriter==3.2.0

  ```

## Setup

1. **Install Python 3.x** : Ensure Python 3.x is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
2. **Use install_venv.bat:** Run the script to set up the virtual environment automatically.
3. **If there are any issues with the script, follow these steps:**

   1. **Install venv (virtual environment) using Pip:**
      `pip install venv`
   2. **Create and setup the virtual environment:** In the directory, open the terminal and do the following:

      1. Create a venv folder:
         `python -m venv venv `
      2. **Open** the venv in powershell:
         `.\venv\Scripts\Activate.ps1  `
         If there are any issues with running scripts being disabled. Use the following command:
         `Set-ExecutionPolicy Unrestricted -Scope Process`
      3. **Install** required libraries: Open a terminal and run the following to install the libraries needed for the program:
         `pip install -r requirements.txt`
4. **Ensure file structure:** Ensure your working directory has the following structure:

   ```
      ├── template/
      │   └── Template.pptx
      ├── images/
      │   └── hardcut.py
      │   └── nypd.ico
      │   └── nypdsplash.png
      ├── src/
      │   └── __main__.py
      │   └── boroBreakdown.py
      │   └── boroSummary.py
      │   └── calculations.py
      │   └── clean.py
      │   └── cwBreakdown.py
      │   └── cwSummary.py
      │   └── output.py
      │   └── overviewPpt.py
      │   └── read.py
      │   └── filter.py
      ├── .gitignore
      ├── install_venv.bat
      ├── LICENSE
      ├── README.md
      ├── standalone_make.bat
      ├── venv_pwsh.bat
      └── requirements.txt

   ```

   5. **Create the application using PyInstaller:** Use the standalone_make.bat script or run the following in the virtual environment's shell:
      `pyinstaller -F --hidden-import "babel.numbers" --hidden-import "openpyxl.cell._writer" --icon=./images/nypd.ico --add-data "images/nypd.ico;." --splash "images/nypdsplash.png" --onefile --noconsole --name ForceStatGen src/__main__.py`

## Usage

1. **Launch the Application** :
   Run the application by double clicking the exe located in the /dist/ folder

   ```
      └── dist/
          └── ForceStatGen.exe
   ```
2. **Select Data Files** :

* Click the buttons to browse and select the required data files: Incident File, Interaction File, and Arrests File.

3. **Select Date Range** :

* Choose between a default span (28 days before the end date) or a custom date range.
* Click on the date entry fields to open a calendar for date selection.

4. **Select Reporting Scope** :

* Check the 'CityWide' checkbox for citywide reports.
* Select individual boroughs for borough-specific reports.

5. **Generate Report** :

* Click the "Generate Report" button to start the process. The application will process the data and generate the reports.

6. **View Output** :

* The generated reports will be saved in the `/output` directory. The Excel report and PowerPoint presentation (if applicable) will be available for review.

## Troubleshooting

* **Permission Errors** : Ensure that all output files are closed before running the application.
* **Missing Template** : If the PowerPoint template is missing, the application will skip the presentation generation step.

## License

This project is licensed under the MIT License.

---

ForceStatGen - Making NYPD reporting efficient and effective.
