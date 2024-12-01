
import torch
import kagglehub
import pandas as pd
import time
import yfinance as yf
import glob
from sklearn.preprocessing import  LabelEncoder, MinMaxScaler
from torch.utils.data import  DataLoader
#from transformers import AutoTokenizer,  AutoModelForSequenceClassification
from torch.nn.functional import softmax
from requests_ratelimiter import LimiterSession, RequestRate, Limiter, Duration


def get_data_from_kaggle(market = 'sp500', start_date = '01-01-2010' ):

    path = kagglehub.dataset_download("paultimothymooney/stock-market-data")
    path_to_files = path + f"\\stock_market_data\\{market}\\csv\\*.csv"

    csv_files = glob.glob(path_to_files)
    dataframes = []

    for file in csv_files:
        stock = file.split("\\")[-1].replace(".csv", "")

        df = pd.read_csv(file)
        df['Stock Name'] = stock
        
        dataframes.append(df)
    stock_df = pd.concat(dataframes, ignore_index=True)
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stock_df = stock_df[stock_df['Date'] >= start_date]
    return stock_df

def restructure_date_information(df):
    df["Month"] = pd.to_datetime(df['Date']).dt.month 
    df["Month"] = df["Month"]- 1
    df["Day"] = pd.to_datetime(df['Date']).dt.day
    df["Day"] = df["Day"]- 1
    df["Day of The Year"] = df["Date"].dt.dayofyear
    df["Day of The Week"] = pd.to_datetime(df['Date']).dt.dayofweek
    df["Week of The Year"] = pd.to_datetime(df['Date']).dt.isocalendar().week
    df["Week of The Year"] = df["Week of The Year"]- 1
    df = df.drop('Date', axis=1, inplace=False)
    return df

def get_static_df(stock_df, static_variables):
    stock_list = stock_df["Stock Name"].unique()
    static_info = {}

    limiter = Limiter(RequestRate(5, 1))
    session = LimiterSession(limiter=limiter)
    for stock in stock_list:
        stock = yf.Ticker(stock, session=session)
        info = stock.info
        selected_info = {var: info.get(var, None) for var in static_variables.keys()}
        static_info[stock.ticker] = selected_info
    static_df = pd.DataFrame.from_dict(static_info).T
    static_df.fillna(0, inplace=True)
    return static_df

def scale_stock_data(stock_df, column):
    scalar = {}
    scaled_data = [] 
    for stock in stock_df["Stock Name"].unique():
        scaler = MinMaxScaler()
        stock_data = stock_df[stock_df['Stock Name'] == stock].copy()
        stock_data[column] = scaler.fit_transform(stock_data[column])
        scaled_data.append(stock_data)
        scalar[stock] = scaler
    out_df = pd.concat(scaled_data, ignore_index=True)
    return out_df, scalar

def stock_quantiles(df, quantiles):
    result = df.groupby("Stock Name")["Adj Close"].quantile(quantiles).unstack()
    result.columns = [f"q_{int(q*100)}" for q in quantiles]
    return result

def one_label_scale_static_df(static_df, static_variables):
    cat_variable =  [variable  for variable, value  in static_variables.items() if value == 'Categorical']
    num_variable =  [variable  for variable, value  in static_variables.items() if value == 'Numerical']
    for variable in cat_variable:
        le = LabelEncoder()
        static_df[variable] = le.fit_transform(static_df[variable].astype(str))

    scaler = MinMaxScaler()
    static_df[num_variable] = scaler.fit_transform(static_df[num_variable])

    return static_df


def get_feature_length(df, constant):
    cat_variable =  [variable  for variable, value  in constant.items() if value == 'Categorical']
    num_variable =  [variable  for variable, value  in constant.items() if value == 'Numerical']
    cat_variable_list = []
    for variable in cat_variable:
        cat_variable_list.append(len(df[variable].unique()))

    return cat_variable_list, len(num_variable)




