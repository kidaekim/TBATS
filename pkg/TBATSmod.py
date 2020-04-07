from tbats import TBATS
from datetime import date
from tsmetrics import tsmetrics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def saveforecast(df1, df2, df3, file_name):

    writer = pd.ExcelWriter(file_name + '.xlsx', engine='xlsxwriter')

    df1.to_excel(writer, sheet_name='Forecast')
    df2.to_excel(writer, sheet_name='Lower_bound')
    df3.to_excel(writer, sheet_name='Upper_bound')

    writer.save()

#==============================================================================  
    
def save_individual_graph(train_df, test_df, forecast_df, ub_df, lb_df):
    train_date = train_df.columns.values
    test_date = test_df.columns.values
    train_date = pd.to_datetime(train_date, format='%m/%Y')
    test_date = pd.to_datetime(test_date, format='%m/%Y')
    
    for index in forecast_df.index.values:
        mae = tsmetrics.mean_absolute_error(
                test_df.loc[index].values, 
                forecast_df.loc[index].values)
        rmse = tsmetrics.root_mean_squared_error(
                test_df.loc[index].values, 
                forecast_df.loc[index].values)
                
        fig, ax = plt.subplots()
        ax.plot_date(train_date, train_df.loc[index], color='red', ls='-',
                     marker=',')
        ax.plot_date(test_date, test_df.loc[index], color='red', ls='-',
                     marker=',', label = 'Actual Data')
        ax.plot_date(test_date, forecast_df.loc[index], color='navy', ls='-',
                     marker=',', label = 'Mean Forecast')
        ax.plot_date(test_date, ub_df.loc[index], color='blue', ls='--',
                     marker=',', label = '90% Confidence Interval')
        ax.plot_date(test_date, lb_df.loc[index], color='blue', ls='--', 
                     marker=',')
        ax.axvline(x=pd.to_datetime(test_date[0], format='%m/%Y'),
                   ls='--', color='black')
        ax.legend()

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.gcf().autofmt_xdate() 
        
        title = index + '(MAE:' + str(round(mae, 3)) + ', RMSE:' + str(round(rmse, 3)) + ')'
        plt.title(title)
        #plt.show()
        
        plt.savefig(index + '.png', bbox_inches='tight')
        
#==============================================================================
        
def error_dict(true_df, forecast_df, error_type):
    result_dict = {}
    if error_type == 'mae': 
        for index in forecast_df.index.values: 
            result_dict[index] = tsmetrics.mean_absolute_error(
            true_df.loc[index].values, 
            forecast_df.loc[index].values)
            
    elif error_type == 'rmse':
        for index in forecast_df.index.values: 
            result_dict[index] = tsmetrics.root_mean_squared_error(
            true_df.loc[index].values, 
            forecast_df.loc[index].values)

    return(result_dict)      