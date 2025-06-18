
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 13:38:06 2023

@author: tamme
"""
import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay
from datetime import datetime
import sys

# Load Tickers and dates from file
#tkrs=pd.read_excel(r'exlConfig.xlsx',sheet_name='Config',usecols='B:B')
#dates=pd.read_excel(r'exlConfig.xlsx',sheet_name='Config',nrows=1,usecols='F:H')
tkrs=pd.read_csv(r'DailyPricesConfig.csv',usecols=['Tickers'])
dates=pd.read_csv(r'DailyPricesConfig.csv',nrows=1,usecols=['StartDate','EndDate','Override'])
tkrs=tkrs['Tickers'].values.tolist()
#tkrs=['TCS.NS','INFY.NS']
#print(tkrs)
overRide=dates['Override'].values.tolist()
overRide=overRide[0]
current_date = pd.Timestamp.now().normalize()
# Determine the dates for which data has to be downloaded

if len(sys.argv) < 3:
    if overRide.upper()=='Y':
        last_working_date = current_date - BDay(0)    
        last_working_date=last_working_date.strftime('%Y-%m-%d')    
        end_date = last_working_date
        last_working_date = current_date - BDay(7)    
        last_working_date=last_working_date.strftime('%Y-%m-%d')    
        start_date = last_working_date
    else:    
        dates
        start_date = dates['StartDate'].tolist()
        end_date = dates['EndDate'].tolist()
        start_date = datetime.strptime(start_date[0], '%d-%m-%Y').strftime('%Y-%m-%d')    
        end_date = datetime.strptime(end_date[0], '%d-%m-%Y').strftime('%Y-%m-%d')   
else:
		arg1 = sys.argv[1]
		arg2 = sys.argv[2]        
		start_date = datetime.strptime(arg1, '%d-%m-%Y').strftime('%Y-%m-%d')    
		end_date = datetime.strptime(arg2, '%d-%m-%Y').strftime('%Y-%m-%d')

i=0

dataset=pd.DataFrame()
yearly_avg_prices=pd.DataFrame()
dataset = yf.download(tkrs, start=start_date, end=end_date, auto_adjust=False,multi_level_index=False)
'''
# Download historical data for each ticker
for tkr in tkrs:
    print(tkr,"\t",i)
    data = yf.download(tkr, start=start_date, end=end_date, auto_adjust=False,multi_level_index=False)      
    data.rename(columns={'Close':tkr},inplace=True)
    #print(data[tkr])
    #dataset = dataset.droplevel(level=0)
    #print(dataset)     
    if len(dataset)>0: dataset=pd.merge(dataset,data[tkr],left_index=True,right_index=True,how='outer')
    else: dataset=data    
    i+=1
'''
dailydata=dataset.copy()
dataset=dailydata.copy()
dataset.drop(['Open','High','Low','Adj Close','Volume'],axis=1,inplace=True)
dataset.index=dataset.index.date
dataset.columns = dataset.columns.droplevel(level=0)
dataset.rename_axis('',axis='columns', inplace=True)
dataset.T.to_excel(r'DailyPrices.xlsx',index='False')
