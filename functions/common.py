from PyPDF2 import PdfReader
import pandas as pd
import openpyxl

from path import path
from functions.sql_connector import c 

# функция определения банка в pdf файле
def bank_finder(src):
    file = open(src, 'rb')
    reader = PdfReader(file)
    text = ''
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()
    work = text
    work = work.split('\n')
    if 'втб' in work[-2].lower():
        return 'втб'
    elif 'тинькофф' in work[7].lower():
        return 'тинькофф'
    return 'others'
    file.close()


# Функция для обработки эксель файлов в формате от Кати Сапожниковой
# Можно сделать в 4 строки через pd.read_excel(), но лень переписывать назад
def xls_converter(src):
    f = openpyxl.load_workbook(src)
    ws = f.active
    data = ws.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа']).dt.date
    df = df.reset_index(drop=True)
    df.columns = (['date', 'description',
                   'summ', 'cat', 'subcat', 'bank', 'type'])
    df['income'] = \
        df.apply(lambda cell: cell.summ if cell.type == 'доход' else 0, axis=1)
    df['expend'] = (df.apply(lambda cell:
                             cell.summ if cell.type == 'расход'
                             else 0, axis=1))
    df = df[['date', 'income', 'expend', 'description', 'bank']]
    df.to_csv(f'/{path}/files/bank_data.csv')
    df_message = f'Добавлено {df.shape[0]} записей.'
    return df_message


# выделить месяцы и годы из базы данных
def get_dates_from_data(name):
    dates = c.execute(f'SELECT DISTINCT(date) FROM {name};').fetchall()
    months = []
    years = []
    for el in dates:
        el = str(el[0]).split('-')
        if el[0] not in years:
            years.append(el[0])
        if el[1] not in months:
            months.append(el[1])
    print(months, years)
    return [months, years]
