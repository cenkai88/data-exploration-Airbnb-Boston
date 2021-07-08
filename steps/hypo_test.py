import pandas as pd

from scipy.stats import fisher_exact
from scipy.stats import mannwhitneyu

def fisher_test(df_high, df_low, columns, alternative='GREATER'):
  '''
    INPUT
    df_high - df of high availability properties
    df_low - df of low availability properties
    columns - columns to make hypothesis test against between two groups
    alternative - enum: ['GREATER', 'LESS'] the test parameter
    
    OUTPUT
    p value of the test
    '''
  dummy_pval = pd.Series()
  for col in columns:
      high_1 = df_high[col].sum()
      high_0 = df_high.shape[0] - high_1
      low_1 = df_low[col].sum()
      low_0 = df_low.shape[0] - low_1
      dummy_pval[col] = fisher_exact([[high_1, high_0], [low_1, low_0]], alternative=alternative)[1]
  
  dummy_pval = dummy_pval[dummy_pval<0.01]
  return dummy_pval

def mannwhitneyu_test(df_high, df_low, columns, alternative):
  '''
    INPUT
    df_high - df of high availability properties
    df_low - df of low availability properties
    columns - columns to make hypothesis test against between two groups
    alternative - enum: ['GREATER', 'LESS'] the test parameter
    
    OUTPUT
    p value of the test
    '''
  numeric_pval = pd.Series()
  for col in columns:
      high = df_high[col]
      low = df_low[col]
      numeric_pval[col] = mannwhitneyu(high, low, alternative=alternative)[1]
  
  numeric_pval = numeric_pval[numeric_pval<0.01]
  return numeric_pval