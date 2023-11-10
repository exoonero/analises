#import functions
import json
import pandas as pd
from pathlib import Path
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import functions

Path = (".")

def get_data(path):
    pop = pd.read_excel(f"{path}/dados/pop_2021.xls", skiprows=1, sheet_name='Municípios', converters={'COD. UF': str, 'COD. MUNIC': str})

    new_df = functions.new_concat(pop, 'cod_mun', 'COD. UF', 'COD. MUNIC')
    new_df = new_df[new_df['UF'] == 'AL']
    new_df['NOME DO MUNICÍPIO'] = new_df['NOME DO MUNICÍPIO'].str.lower()
    new_df = new_df.replace({' ': '-'}, regex=True)
    new_df = new_df.rename(columns={'UF': 'uf', 'COD. UF': 'cod_uf', 'COD. MUNIC': 'cod_mun_old',
                                    'NOME DO MUNICÍPIO': 'nome_mun', 'POPULAÇÃO ESTIMADA': 'pop_estim'})

    df_zip = pd.read_json(f"{path}/df.zip")
    df = pd.merge(new_df, df_zip, how='left', left_on='nome_mun', right_on='municipio')

    new_df = df.groupby(['cod_mun', 'ano'])[['num_nomeacoes', 'num_exoneracoes']].sum().reset_index()
    serie_pop = df[['cod_mun', 'pop_estim']].drop_duplicates()
    new_df = pd.merge(serie_pop, new_df, on='cod_mun', how='inner')

    return new_df

pop = pd.read_excel(".\dados\pop_2021.xls", skiprows=1, sheet_name='Municípios', converters={'COD. UF': str, 'COD. MUNIC': str})

new_df = functions.new_concat(pop, 'cod_mun', 'COD. UF', 'COD. MUNIC')
new_df = new_df[new_df['UF'] == 'AL']
new_df['NOME DO MUNICÍPIO'] = new_df['NOME DO MUNICÍPIO'].str.lower()
new_df = new_df.replace({' ': '-'}, regex=True)
new_df = new_df.rename(columns={'UF': 'uf', 'COD. UF': 'cod_uf', 'COD. MUNIC': 'cod_mun_old',
                                'NOME DO MUNICÍPIO': 'nome_mun', 'POPULAÇÃO ESTIMADA': 'pop_estim'})

 
df_zip = pd.read_json(".\df.zip")
#print(df_zip.head())
df = pd.merge(new_df, df_zip, how='left', left_on='nome_mun', right_on='municipio')

new_df = df.groupby(['cod_mun', 'ano'])[['num_nomeacoes', 'num_exoneracoes']].sum().reset_index()
serie_pop = df[['cod_mun', 'pop_estim']].drop_duplicates()
new_df = pd.merge(serie_pop, new_df, on='cod_mun', how='inner')

print(new_df.head(10))

#### SEPARANDO AS CIDADES POR CLUSTERS #####
#1° observando a média e mediana da população
print(np.mean(new_df['pop_estim']))
print(np.median(new_df['pop_estim']))

#data = new_df['pop_estim']
#fig = plt.figure(figsize =(10, 7))
#plt.boxplot(new_df['pop_estim'])
#plt.show()

df_c1 = new_df[new_df['pop_estim'] < 20000]
df_c2 = new_df[(new_df['pop_estim'] >= 20000) | (new_df['pop_estim'] < 35000)]
df_c3 = new_df[(new_df['pop_estim'] >= 35000) | (new_df['pop_estim'] < 50000) ]
df_c4 = new_df[(new_df['pop_estim'] >= 50000) | (new_df['pop_estim'] < 65000) ]
df_c5 = new_df[(new_df['pop_estim'] >= 65000)]

#print(df_c1.head())
#print(d)f_c2.head())    
#print(df_c3.head())
#print(df_c4.head())
#print(df_c5.head())
###
def find_outliers_IQR(df, column):
    q1=df[column].quantile(0.25)
    q3=df[column].quantile(0.75)
    IQR=q3-q1
    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
    
    return outliers

#outliers = find_outliers_IQR(new_df, "cod_mun")
#print(outliers)

## Integrar com:
## RAIS /CAGED
## https://dadosabertos.camara.leg.br/swagger/api.html

