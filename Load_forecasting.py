# @author: Ana Jevtic and Stefanos Baros (both authors contributed equally)


# import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# from sklearn.impute import SimpleImputer
# from scipy.stats.stats import pearsonr   
import matplotlib.pyplot as plt
# import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

main_folder = "/Users/stefanosbaros/Desktop/Load_forecasting_ver2/"
 
        
baseline = pd.read_csv(main_folder + "baseline_model_data.csv", index_col=0)
full_model = pd.read_csv(main_folder + "full_model_data.csv", index_col=0)


baseline.dropna(axis=0, inplace=True)
full_model.dropna(axis=0, inplace=True)

years=baseline.year.unique()

# print(years[4]) # 2004-2007 train data; 2008 test data

feature_list=[]


feature_list.append(['TREND','TMP','TMP2'])
feature_list.append(['TREND','TMP','TMP2','TMP3'])
feature_list.append(['TREND','TMP','TMP2','TMP3','SIN_MONTH','COS_MONTH'])
feature_list.append(['TREND','TMP','TMP2','TMP3','SIN_MONTH','COS_MONTH', 'DTMPxSIN_HOUR', 'DTMPxCOS_HOUR'])
feature_list.append(['TREND','TMP','TMP2','TMP3','SIN_MONTH','COS_MONTH','TMPxSIN_MONTH',
            'TMPxCOS_MONTH','TMP2xSIN_MONTH','TMP2xCOS_MONTH', 'TMP3xSIN_MONTH','TMP3xCOS_MONTH'])
feature_list.append(['TREND','TMP','TMP2','TMP3','SIN_MONTH','COS_MONTH','TMPxSIN_MONTH',
            'TMPxCOS_MONTH','TMP2xSIN_MONTH','TMP2xCOS_MONTH', 'TMP3xSIN_MONTH','TMP3xCOS_MONTH','DTMPxSIN_HOUR', 'DTMPxCOS_HOUR'])
feature_list.append(['TREND','TMP','TMP2','TMP3','SIN_MONTH','COS_MONTH','TMPxSIN_MONTH',
            'TMPxCOS_MONTH','TMP2xSIN_MONTH','TMP2xCOS_MONTH', 'TMP3xSIN_MONTH','TMP3xCOS_MONTH',
            'TMPxSIN_HOUR','TMPxCOS_HOUR','TMP2xSIN_HOUR','TMP2xCOS_HOUR', 'TMP3xSIN_HOUR','TMP3xCOS_HOUR',
            'DTMPxSIN_HOUR', 'DTMPxCOS_HOUR','Holi','isWknd'])



for features in feature_list:
    
    X_train= full_model.loc[full_model.year.isin(years[0:4])][features]
    y_train= full_model.loc[full_model.year.isin(years[0:4])].LOAD
    
    
    X_test = full_model.loc[full_model.year == years[4]][features]
    y_test= full_model.loc[full_model.year == years[4]].LOAD
    
    
    # # Multiple linear regression 
    lr=LinearRegression()
    lr.fit(X_train,y_train)
    y_pred=lr.predict(X_test)
    
    
    
    # # plotting Load vs Temperature 
    plt.scatter(y_test,X_test.TMP, linestyle='-',label='actual')
    plt.scatter(y_pred,X_test.TMP,color='green', linestyle='dashed',label='predicted')
    plt.xlabel('load')
    plt.ylabel('temperature')
    plt.title('Actual and predicted load vs Temperature')
    plt.legend(loc='upper left');
    plt.show()
    
    
    
    # Actual vs Predicted load baseline model
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=3)
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    plt.show()
    
    
    
    
    
    ### Diagnostic Statistics
    
    ## Goodness-of-fit
    # Adjusted R2 baseline model
    r2 = r2_score(y_test, y_pred)
    r2_adj = 1 - (1-r2)*(len(y_train)-1)/(len(y_train)-X_train.shape[1]-1)
    print("Adjusted R^2 for the model: ", r2_adj)
    
    # MAPE
    
    # STDAPE
    
    ## Accuracy
    
    # MAPE baseline model
    # MAPE_out = mean_absolute_percentage_error(y_test, y_pred)
    # print("MAPE for the baseline model: ", MAPE_out)
    
    # # MAPE full model
    # MAPE_out_full = mean_absolute_percentage_error(y_test_full, y_pred_full)
    # print("MAPE for the full model: ", MAPE_out_full)
    
    
      # MAE baseline model
    MSE = mean_squared_error(y_test,y_pred)
    print("MSE for the model: ", MSE)
    
    # MAE baseline model
    MAE = mean_absolute_error(y_test,y_pred)
    print("MAE for the model: ", MAE)
    
    
    # # # plotting Load vs Temperature^2
    # Temp_squared=np.square(station_temp_hourdata_imp.iloc[:,-1:])
    # plt.scatter(Load,Temp_squared,linestyle='-',label='actual')
    # plt.xlabel('load')
    # plt.ylabel('temperature')
    # plt.title('vs T^2')
    # plt.legend(loc='upper left');
    # plt.show()
    
    # # # plotting Load vs Temperature^3
    # Temp_cube=np.power(station_temp_hourdata_imp.iloc[:,-1:],3)
    # plt.scatter(Load,Temp_cube,linestyle='-',label='actual')
    # plt.xlabel('load')
    # plt.ylabel('temperature')
    # plt.title('vs T^3')
    # plt.legend(loc='upper left');
    # plt.show()
    
    # # # calculating correlation between station 1 temperature and zone 1 load
    # # data=np.concatenate([zone_load_hourdata_imp,station_temp_hourdata_imp],axis=1)
    # # r= np.corrcoef(data, rowvar=False)
    # # print(r)
    
    
    # lr=LinearRegression()
    # lr.fit(Temp,Load)
    # Load_pred=lr.predict(Temp)
    
    # # plotting Predicted Load vs Temperature (regression line)
    # plt.scatter(Load_pred,y_test,color='green', linestyle='dashed',label='actual')
    # plt.xlabel('load')
    # plt.ylabel('temperature')
    # plt.title('Predicted Load')
    # plt.legend(loc='upper left');
    # plt.show()



