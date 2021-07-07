import pandas as pd

from utils.formatter import currency_formatter
from utils.formatter import daterange_formatter

def process_zipcode(df):
  '''
    INPUT
    df - the original dataframe
    This function groups zipcode to calculate a median price for zipcode indicating 
    the overall price for a certain area(`zipcode_median_price`).
    And create `relative_zipcode_price` = `zipcode_median_price` / `price` to 
    indicate if an item is more expensive or cheaper than the most other items
    in the area.
    This will drop the zipcode column.

    OUTPUT
    the updated df
  '''
  df['zipcode'] = df['zipcode'].apply(
      lambda x: str(x).split('-')[0].split(' ')[0])
  zipcode_median_price = df[['zipcode', 'price']].groupby(
      'zipcode').agg('median')
  df['zipcode_median_price'] = df['zipcode'].apply(
      lambda x: zipcode_median_price['price'][x])
  df['relative_zipcode_price'] = df['price'] / \
      df['zipcode_median_price']
  df.drop(['zipcode'], axis=1, inplace=True)
       
  return df

def process_amenities(df):
  '''
    INPUT
    df - the original dataframe
    This function format amenities column into multiple columns so that
    it can be processed by generate_dummies function
    This will drop the amenities column.

    OUTPUT
    the updated df
  '''
  amenities = set()
  for i in range(df.shape[0]):
      amenities.update(list(map(lambda x: x.strip(
          '"'), df['amenities'][i].strip('{').strip('}').split(','))))

  for amenty in list(amenities):
      if len(amenities) == 0:
          continue
      df['amenities_'+amenty.replace(' ', '_')] = df['amenities'].apply(
          lambda record: amenty in list(map(lambda x: x.strip('"'), record.strip('{').strip('}').split(','))))

  df.drop(['amenities'], axis=1, inplace=True)
       
  return df

def generate_dummies(df):
  '''
    INPUT
    df - the original dataframe
    This function create the dummies columns and remove the original categorical 
    columns.

    OUTPUT
    the updated df
  '''
  for col in df.select_dtypes(include=['object']).columns:
      try:
          df = pd.concat([df.drop(col, axis=1), pd.get_dummies(
              df[col], prefix=col, prefix_sep='_')], axis=1)
      except:
          print(col)
          continue
       
  return df

def drop_nas(df, columns):
  '''
    INPUT
    df - the original dataframe
    columns - columns to drop

    OUTPUT
    the updated df
  '''
  df = df.dropna(axis=1, how='all')
  for col in columns:
    df.drop([col], axis=1, inplace=True)
  
  return df

def convert_to_bool(df, columns):
  '''
    INPUT
    df - the original dataframe
    columns - columns to convert to bool, including col name and truthy_value 
              which is the value needed to be considered as true.
              if truthy_value is set as False, values that are not null will be converted to True

    OUTPUT
    the updated df
  '''
  for col in columns:
    name, truthy_value = col
    convert_fn = (lambda x: x == truthy_value) if truthy_value else (lambda x: pd.notnull(x))
    df[name] = df[name].apply(convert_fn)
  
  return df


def convert_to_num(df, columns):
  '''
    INPUT
    df - the original dataframe
    columns - columns to convert to bool, including col name and category
              including: CURRENCY, DATERANGE, PERCENT, TEXTLENGTH

    OUTPUT
    the updated df
  '''
  for col in columns:
    name, category = col
    if (category == 'CURRENCY'):
      convert_fn = currency_formatter
      df[name] = df[name].apply(convert_fn)
      df[name].fillna(0, inplace=True)
    elif (category == 'DATERANGE'):
      convert_fn = daterange_formatter
      df[name] = df[name].apply(convert_fn)
      max_date_delta = df[name].max()
      df[name].fillna(max_date_delta, inplace=True)
    elif (category == 'PERCENT'):
      df[name] = df[name].apply(
        lambda x : x if pd.isna(x) else int(x.strip('%')) / 100)
      df[name].fillna(df[name].median(), inplace=True)
    elif (category == 'TEXTLENGTH'):
      df[name] = df[name].apply(
        lambda x : x if pd.isna(x) else len(x))
       
  return df

def fill_col_na(df, columns):
  '''
    INPUT
    df - the original dataframe
    columns - columns to convert to bool, including col name, default value 

    OUTPUT
    the updated df
  '''
  for col in columns:
    name, value = col
    df[name].fillna(value, inplace=True)
       
  return df


