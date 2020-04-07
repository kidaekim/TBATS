from tbats import TBATS
from datetime import date
from tsmetrics import tsmetrics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from scipy.signal import savgol_filter
from pkg.TBATSmod import saveforecast, save_individual_graph

#============================================================================== 
# Forecast Model appliaction and save.

train_df = pd.read_excel('train.xlsx', index_col=0)

y_forecast = {}
lower_int = {}
upper_int = {}

if __name__ == '__main__':
    estimator = TBATS(seasonal_periods=[12])
     
    for index in train_df.index.values: 
        fitted_model = estimator.fit(train_df.loc[index])
        y_forecasted, confidence_int = fitted_model.forecast(steps=12,
                                                             confidence_level=0.90)
        
        y_forecast[index] = confidence_int['mean']
        lower_int[index] = confidence_int['lower_bound']
        upper_int[index] = confidence_int['upper_bound']
        
saveforecast(pd.DataFrame(y_forecast).T,
             pd.DataFrame(lower_int).T,
             pd.DataFrame(upper_int).T, 
             'forecast')

#============================================================================== 
# Produce graphs based on the forecast 

train_df = pd.read_excel('train.xlsx', index_col=0)
test_df = pd.read_excel('test.xlsx', index_col=0)
forecast_df = pd.read_excel('forecast.xlsx', sheet_name=0, index_col=0)
lb_df = pd.read_excel('forecast.xlsx', sheet_name=1, index_col=0)
ub_df = pd.read_excel('forecast.xlsx', sheet_name=2, index_col=0)

save_individual_graph(train_df, test_df, forecast_df, lb_df, ub_df)

#==============================================================================
# Savitzky-Golay filter example

filtered_train_df = pd.DataFrame(savgol_filter(train_df, window_length=5, polyorder=2))
filtered_train_df.index = train_df.index
filtered_train_df.columns = train_df.columns

#==============================================================================
