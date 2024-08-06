# libraries
import sys
from xlsx2csv import Xlsx2csv
from io import StringIO
from pandas import read_csv
from pandas import DataFrame

def read_excel(path: str) -> DataFrame:
    buffer = StringIO()
    Xlsx2csv(path, outputencoding="utf-8" ).convert(buffer)
    buffer.seek(0)
    df = read_csv(buffer, low_memory=False, thousands=',')
    return df

def readData(fp1, fp2, fp3):
    file_paths = {'incall': fp1, 'intall': fp2, 'arrests': fp3}
    results = {}

    for key, file_path in file_paths.items():
        if file_path.endswith(('xlsx', 'xls')):
            results[key] = read_excel(file_path)
        else:
            try:
                results[key] = read_csv(file_path, low_memory=False, thousands=',')
            except Exception:
                results[key] = read_csv(file_path, low_memory=False, thousands=',', encoding='utf-16', sep='\t')

    return results['incall'], results['intall'], results['arrests']