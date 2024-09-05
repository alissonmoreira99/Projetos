import pandas
import re

def filter_columns(df, filters: list): # adiciono no array o padrão que existe nas colunas e que não quero que tenha na saída final
    selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
    for index, column in enumerate(df.columns):
        if any(filter in column for filter in filters): selected_columns[index] = False
    return df[df.columns[selected_columns]]

def cleaning_dataset(df):
  _df = df.dropna(subset=df.columns.difference(['NOME']), how='all') # executa o dropna para todas as colunas sem visualizar a coluna NOME
  _df = _df[~_df.isna().all(axis=1)] # remove linhas com apenas NaN, se tiver algum dado na linha não remove
  return _df


def faixa_etaria(idade):
  faixa = ''
  if idade >= 7 and idade <= 9:
    faixa = '7 a 9'
  elif idade >= 10 and idade <= 12:
    faixa = '10 a 12'
  elif idade >= 13 and idade <= 15:
    faixa = '13 a 15'
  elif idade >= 16 and idade <= 18:
    faixa = '16 a 18'
  elif idade >= 19 and idade <= 21:
    faixa = '19 a 21'
  return faixa


def transform_column(column):
  column = column.transform(lambda x: x.replace(',', '.'))
  column = column.astype(float)
  return column

def treat_columns(text):
    text = text.replace('_','')
    return re.sub(r'\d+', '', text)

def arredondar_numericos(df):
    # Selecionar apenas as colunas numéricas
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Arredondar para 2 casas decimais
    df[colunas_numericas] = df[colunas_numericas].round(2)
    
    return df