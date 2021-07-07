import pandas as pd

from sklearn.ensemble import RandomForestRegressor

def optimize_param(X_train, y_train):
  '''
    INPUT
    X_train - dependent variable
    y_train - independent variable
    This function shows the plot of number of trees with model score 
    to help user pick the suitable n_estimator

    '''
  # the suitable n_estimator
  results_rf = []
  n_estimator_options = [20, 30, 50, 100, 200, 500, 1000]

  for trees in n_estimator_options:
      model = RandomForestRegressor(trees,oob_score=True,n_jobs=-1,random_state=42)
      model.fit(X_train,y_train)
      print(trees," trees")
      score = model.score(X_train,y_train)
      print(score)
      results_rf.append(score)
      print("")

  fig = pd.Series(results_rf,n_estimator_options).plot().get_figure()
  fig.savefig('images/model-optimize.jpg')

