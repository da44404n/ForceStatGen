# WRITING THE DATAFRAMES TO AN EXCEL SHEET

# needs to be center alignment
# calibri font
# 7.5 font size
# libraries
# from typing import List

from pandas import ExcelWriter
from numpy import where

import io
import openpyxl as openpyxl
from openpyxl.styles import Font, Alignment

def outputToExcel(tables_dict, filePath):
    with ExcelWriter(filePath, engine='openpyxl', mode='w') as writer:
        for sheet_name, tables in tables_dict.items():
            prev_height = 0  # Initialize the starting row for the first table

            for table in tables:
                table = table.apply(lambda x: x.apply(lambda y: '{:,}'.format(y) if type(y) == int else y))
                
                table = table.astype(str).replace({
                    # 'nan': '***',
                    'nan': '',
                    'nan%': '***',
                    'inf': '***',
                    'inf%': '***',
                    # 'None': '***'
                    'None': ''
                })

                # Write each table to the same sheet, starting at the row indicated by prev_height
                table.to_excel(writer, sheet_name=sheet_name, startcol=0, startrow=prev_height, index=True)
                
                # Update prev_height to be below the current table, adding 3 for spacing
                prev_height += len(table.index) + 3

    # in_mem_file is used to store the file in memory because there is a bug with openpyxl that causes the file to remain open.
    in_mem_file = None
    with open(filePath, "rb") as f:
        in_mem_file = io.BytesIO(f.read())

    # Open the workbook to apply styles
    workbook = openpyxl.load_workbook(in_mem_file)
    
    # Apply styles to each sheet
    font = Font(name='Calibri', size=7.5)
    alignment = Alignment(horizontal='center', vertical='center')

    for sheet_name in tables_dict.keys():
        worksheet = workbook[sheet_name]
        for row in worksheet.iter_rows():
            for cell in row:
                cell.font = font
                cell.alignment = alignment

    # Save the workbook with styles applied 
    workbook.save(filePath)
    workbook.close()
    workbook = None