# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:26:00 2020

@author: Ana Jevtic and Stefanos Baros (both authors contributed equally)


Data cleansing and preprocessing for regression
Regression variables:
    1) Baseline model (TREND, TMP, TMP2, TMP3)
    2) Full model (TREND, MONTH, TMP*TMPID*MONTH, TMP2*TMPID*MONTH, TMP*TMPID*HOUR,
               TMP2*TMPID*HOUR, DTMP*TMPID*HOUR, D*HOUR)
Target variable:
    LOAD
"""
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np

# reading data
main_file="C:/Users/Ana/Desktop/Load_Forecasting_Project/"
temp_data = pd.read_csv(main_file + "temperature_history.csv")
load_data = pd.read_csv(main_file + "Load_history_imputed.csv", index_col=0)

# Load 1 and Temperature station 6; correlation coefficient = -0.85 
# stations=[i for i in range(1,12)]

station = 6
temp_st1=temp_data.loc[temp_data.station_id==station]

# Stack the temperature variable to create TMP, add HOUR variable with 24 values

hourly_temp=pd.wide_to_long(temp_st1.iloc[:,1:], ['h'], i=['year','month', 'day'], j='hour')
hourly_temp=hourly_temp.rename(columns={"h":"TMP"})
hourly_temp.reset_index(inplace=True)

# Add load data - LOAD
zone = 1
load_zn1 = load_data.loc[load_data.zone_id==zone]

reg_data_full=pd.merge(hourly_temp,load_zn1, on=['year','month','day','hour'])
reg_data_full.drop('zone_id', axis=1, inplace=True) 

# Add holiday data/ update DW variable

holiday_data = pd.read_csv(main_file + "Holiday_List.csv", index_col=0)

years=pd.DataFrame({col: col for col in list(holiday_data.columns.values)},index=holiday_data.index)

holiday_data = holiday_data + " " + years

f = lambda x: pd.to_datetime(x, format='%A, %B %d %Y')
holiday_data = holiday_data.applymap(f)
holiday_data= holiday_data.reset_index(drop=True)

holiday_data= pd.concat([holiday_data['2004'], holiday_data['2005'],holiday_data['2006'],holiday_data['2007'],holiday_data['2008']])
holiday_data=holiday_data.reset_index(drop=True).dropna()

Holi = pd.DataFrame({'year': holiday_data.dt.year, 'month':holiday_data.dt.month, 'day': holiday_data.dt.day, 'Holi': 1}, index=holiday_data.index)

reg_data_full = pd.merge(left=reg_data_full, right=Holi, how='left', left_on=['year','month','day'], right_on=['year','month','day'])

reg_data_full['Holi'].fillna(0, inplace=True)

# Add T^2 and T^3 variables - TMP2 and TMP3
reg_data_full["TMP2"]=pd.Series(np.square(reg_data_full['TMP'].to_numpy()))
reg_data_full["TMP3"]=pd.Series(np.power(reg_data_full['TMP'].to_numpy(),3))

# Add TREND variable
reg_data_full['TREND']=reg_data_full.index+1

# Add day of the week variable - DW (Mon-Sun <=> 1-7)
reg_data_full['DW']=pd.to_datetime(reg_data_full.loc[:,['year','month','day']]).dt.dayofweek+1

# Add variable to label weekends - isWknd
reg_data_full['isWknd']=(reg_data_full['DW']>=6).astype(float)

# Add temperature difference (DTMP) variable
reg_data_full['DTMP']=reg_data_full['TMP'].diff()
reg_data_full['DTMP']=reg_data_full['DTMP'].fillna(0)


# Convert month/hour to 1-hot/cyclical encoding
# SIN_HOUR and COS_HOUR
reg_data_full['SIN_HOUR'] = np.sin(2*np.pi*reg_data_full.hour/24)
reg_data_full['COS_HOUR'] = np.cos(2*np.pi*reg_data_full.hour/24)


# SIN_MONTH and COS_MONTH
reg_data_full['SIN_MONTH'] = np.sin(2*np.pi*reg_data_full.month/12)
reg_data_full['COS_MONTH'] = np.cos(2*np.pi*reg_data_full.month/12)
 

# Add cross-effect variables
# TMPxMONTH(cyclic)
reg_data_full['TMPxSIN_MONTH'] = reg_data_full['TMP'].multiply(reg_data_full['SIN_MONTH'])
reg_data_full['TMPxCOS_MONTH'] = reg_data_full['TMP'].multiply(reg_data_full['COS_MONTH'])

# TMP2xMONTH(cyclic)
reg_data_full['TMP2xSIN_MONTH'] = reg_data_full['TMP2'].multiply(reg_data_full['SIN_MONTH'])
reg_data_full['TMP2xCOS_MONTH'] = reg_data_full['TMP2'].multiply(reg_data_full['COS_MONTH'])

# TMP3xMONTH(cyclic)
reg_data_full['TMP3xSIN_MONTH'] = reg_data_full['TMP3'].multiply(reg_data_full['SIN_MONTH'])
reg_data_full['TMP3xCOS_MONTH'] = reg_data_full['TMP3'].multiply(reg_data_full['COS_MONTH'])

# TMPxHOUR(cyclic)
reg_data_full['TMPxSIN_HOUR'] = reg_data_full['TMP'].multiply(reg_data_full['SIN_HOUR'])
reg_data_full['TMPxCOS_HOUR'] = reg_data_full['TMP'].multiply(reg_data_full['COS_HOUR'])

# TMP2xHOUR(cyclic)
reg_data_full['TMP2xSIN_HOUR'] = reg_data_full['TMP2'].multiply(reg_data_full['SIN_HOUR'])
reg_data_full['TMP2xCOS_HOUR'] = reg_data_full['TMP2'].multiply(reg_data_full['COS_HOUR'])

# TMP3xHOUR(cyclic)
reg_data_full['TMP3xSIN_HOUR'] = reg_data_full['TMP3'].multiply(reg_data_full['SIN_HOUR'])
reg_data_full['TMP3xCOS_HOUR'] = reg_data_full['TMP3'].multiply(reg_data_full['COS_HOUR'])

# DTMPxHOUR(cyclic)
reg_data_full['DTMPxSIN_HOUR'] = reg_data_full['DTMP'].multiply(reg_data_full['SIN_HOUR'])
reg_data_full['DTMPxCOS_HOUR'] = reg_data_full['DTMP'].multiply(reg_data_full['COS_HOUR'])

# Save to .csv file
reg_data_full.to_csv(main_file + "full_model_data.csv")
