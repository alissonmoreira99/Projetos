import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from prophet import Prophet

def preprocess_data(df):
    df.set_index('Data', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    start = df.index.min()
    end = df.index.max()
    date_range = pd.date_range(start=start, end=end)
    df = df.reindex(date_range)
    df.index.rename('Data', inplace=True)
    df['Preço'] = df['Preço'].fillna(method='ffill')
    return df

# Função para preparar dados para o Prophet
def prepare_for_prophet(df):
    df_data = df.reset_index()
    df = pd.DataFrame()
    df[['ds', 'y']] = df_data[['Data', 'Preço']]
    return df


# Função customizada para combinar processamento e previsão
def process_and_forecast(df):
    # Transformadores customizados
    preprocess_transformer = FunctionTransformer(preprocess_data)
    prepare_transformer = FunctionTransformer(prepare_for_prophet)
    df_processed = preprocess_transformer.transform(df)
    df_prepared = prepare_transformer.transform(df_processed)
    return df_prepared