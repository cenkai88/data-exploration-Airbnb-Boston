import math
import pandas as pd

def format_calendar_data(calendar):
    '''
    INPUT
    calendar - the original dataframe of calendar

    OUTPUT
    price_available_rate - the groupby result of the calendar including
    price_num, price_num_log, available_num
    '''
    
    calendar = calendar.copy()
    calendar.loc[:, 'price_num'] = calendar['price'].apply(
        lambda x: x if pd.isnull(x) else float(x[1:].replace(',', '')))
    calendar.loc[:, 'price_num_log'] = calendar['price'].apply(
        lambda x: x if pd.isnull(x) else math.log(float(x[1:].replace(',', ''))))
    calendar = calendar[((calendar['price_num'] < 1000) & (
        calendar['price_num'] > 20)) | pd.isnull(calendar['price_num'])]
    calendar.loc[:, 'available_num'] = calendar['available'].apply(
        lambda x: 1 if x == 't' else 0)
    price_available_rate = calendar.groupby(['listing_id']).agg({
        'price_num': lambda x: x.mean(skipna=True),
        'price_num_log': lambda x: x.mean(skipna=True),
        'available_num': 'mean'
    })
    return price_available_rate
