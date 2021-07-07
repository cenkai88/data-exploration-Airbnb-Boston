import pandas as pd

from datetime import date

def calendar_updated_formatter(text):
    '''
    INPUT
    text - calendar text
    
    OUTPUT
    formatted calendar text
    
    This function simplify the value of calendar text
    enums are: ['today', 'yesterday', 'within a week', 'within a month', 'more than a month ago']
    '''
    text_splitted = text.split(' ')
    if text=='today' or text=='yesterday': return text
    elif len(text_splitted)>1 and text_splitted[2]=='days': return 'within a week'
    elif len(text_splitted)>1 and text_splitted[2]=='weeks': return 'within a month'
    else: return 'more than a month ago'

def currency_formatter(text):
    '''
    INPUT
    text - text of currency
    
    OUTPUT
    currency as float type
    '''
    return text if pd.isna(text) else float(text.strip('$').replace(',', ''))

def daterange_formatter(text):
    '''
    INPUT
    text - text of date
    
    OUTPUT
    days number between the input date and dataset_created_date
    '''
    dataset_created_date = '2016-11-17'
    return text if pd.isna(text) else (date.fromisoformat(dataset_created_date) - date.fromisoformat(text)).days