import pandas as pd
import requests
from bs4 import BeautifulSoup
import os


def pu_ot(file_name, xls_name):

    # LOG-IN PARAM
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}

    # Getting row information as a temp_file.html
    with requests.Session() as s:
        # Finding the authentication needed to gain access to Pegasus Module
        url = 'https://www.oliveiratrust.com.br/fiduciario/pus_dt.php?ativo=CRI'
        r = s.get(url, headers=headers)

        with open(file_name, 'w') as file:
            file.write(r.text)

    extract_ot = {'Titulo': [],'Emissor': [], 'PU_cheio': [], 'PU_ex': []}

    # Reformating all the row information extracted from the funcking site
    with open(file_name, encoding="ISO-8859-1") as fp:

        soup = BeautifulSoup(fp, 'html.parser')

        for table in soup.find_all('tr'):
            table = table.text.split('\n')

            #######################################################
            titulo = table[1]
            if titulo == 'Titulo': continue
            if titulo == 'Amortização':
                continue

            else:
                extract_ot['Titulo'].append(titulo)
            #######################################################
            emissor = table[2]
            extract_ot['Emissor'].append(emissor)
            #######################################################
            pu = [info for info in table[6:7]]
            for j in pu:
                extract_ot['PU_cheio'].append(j)
            #######################################################
            puex = [ex for ex in table[11:12]]
            for k in puex:
                extract_ot['PU_ex'].append(k)

    df = pd.DataFrame(extract_ot)

    var_01 = df['Titulo'].str.split('(').str[-1]
    var_final = var_01.str.split(')').str[0]

    df['Titulo'] = var_final

    df['PU_cheio'] = df['PU_cheio'].str.replace('.', '*')
    df['PU_cheio'] = df['PU_cheio'].str.replace(',', '.')
    df['PU_cheio'] = df['PU_cheio'].str.replace('*', '')

    df['PU_ex'] = df['PU_ex'].str.replace('.', '*')
    df['PU_ex'] = df['PU_ex'].str.replace(',', '.')
    df['PU_ex'] = df['PU_ex'].str.replace('*', '')

    file_name = f'temp_pu_file.xlsx'
    df.to_excel(f'{file_name}', index=False)

    df_finale = pd.read_excel(f'{file_name}')
    df_finale['delta'] = df_finale['PU_cheio'] - df_finale['PU_ex']

    param01 = [i for i in df_finale['delta'].values]

    result = []

    for info in param01:
        if info > 0:
            result.append('SIM')
        else:
            result.append('-')

    df_finale['PGTO(?)'] = result
    df_finale = df_finale.drop(['delta'], axis=1)

    df_finale.to_excel(xls_name, index=False)
    os.remove(file_name)
