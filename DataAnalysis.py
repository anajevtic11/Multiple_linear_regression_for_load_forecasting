# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:00:14 2020

@author: Ana Jevtic and Stefanos Baros (both authors contributed equally)

Imputation for 8 nonconsecutive weeks of missing load data
Correlation analysis for load zones and temperature stations
"""
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# reading data
main_file="C:/Users/Ana/Desktop/Load_Forecasting_Project/"
load_data = pd.read_csv(main_file + "Load_history.csv", decimal=',')

load_data_imputed=load_data.copy()

hours=load_data.columns[4:]

for hour in hours:
    load_data_imputed[hour] = load_data.groupby(['zone_id','month','day'])[hour].transform(lambda x: x.fillna(x.mean()))

# Stack the temperature variable to create LOAD, add HOUR variable with 24 values

load_data_imputed=pd.wide_to_long(load_data_imputed, ['h'], i=['zone_id','year','month', 'day'], j='hour')
load_data_imputed=load_data_imputed.rename(columns={"h":"LOAD"})
load_data_imputed.reset_index(inplace=True)


load_data_imputed.to_csv(main_file + "Load_history_imputed.csv")

# Correlation analysis load_station vs temp_zone
temp_data = pd.read_csv(main_file + "temperature_history.csv")


stations=temp_data.station_id.unique() #[i for i in range(1,12)]
zones=load_data_imputed.zone_id.unique()

# Stack the temperature variable to create TMP, add HOUR variable with 24 values

hourly_temp=pd.wide_to_long(temp_data, ['h'], i=['station_id','year','month', 'day'], j='hour')
hourly_temp=hourly_temp.rename(columns={"h":"TMP"})
hourly_temp.reset_index(inplace=True)

# Stack the load and temp vectors
corr_matrix=load_data_imputed.loc[load_data_imputed.zone_id==1].LOAD.copy()
corr_matrix.name='L_1'

for zone in zones[1:]:
    corr_matrix=pd.concat([corr_matrix, load_data_imputed.loc[load_data_imputed.zone_id==zone].LOAD.reset_index(drop=True)], axis=1)
    corr_matrix.rename(columns={'LOAD':'L_'+str(zone)}, inplace=True)

for station in stations:
    corr_matrix=pd.concat([corr_matrix, hourly_temp.loc[hourly_temp.station_id==station].TMP.reset_index(drop=True)], axis=1)
    corr_matrix.rename(columns={'TMP':'TMP_'+str(station)}, inplace=True)
    
corr_matrix=corr_matrix.dropna()

# Consider only first 3 months of 2004
correlation_df = corr_matrix.iloc[:2185,:].corr()

print(correlation_df)
