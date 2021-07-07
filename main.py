# %%
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from steps.explore import format_calendar_data
from steps.clean import clean_listings_data
from steps.radom_forest import optimize_param
from steps.hypo_test import fisher_test, mannwhitneyu_test

%matplotlib inline

# %%
# 1. Explore the relationship between availability and price
calendar = pd.read_csv('./dataset/Boston/calendar.csv')
calendar.head()
# format the price column to numeric value, use log to normalize price value and exclude outliners
price_available_rate = format_calendar_data(calendar)

# %%
plt.scatter(price_available_rate['price_num'], price_available_rate['available_num'])

# %%
plt.scatter(price_available_rate['price_num_log'], price_available_rate['available_num'])

# %%
price_available_rate[['price_num_log', 'available_num']].corr()

# 2. Look for factors that effect the availability
# %%
listings = pd.read_csv('./dataset/Boston/listings.csv')
listings = clean_listings_data(listings)
# save data to 
listings.to_csv("./dataset/boston_data_formatted.csv", encoding="utf_8_sig")

# 3. Try to predict the availability using price and other factors (LinearRegression)
# %%
listings_X = listings.drop(['id', 'availability'], axis=1)
listings_y = listings['availability']
X_train, X_test, y_train, y_test = train_test_split(
    listings_X, listings_y, test_size=.2)

linear_model_sm = sm.OLS(y_train,sm.tools.add_constant(X_train).astype(float))
results_sm = linear_model_sm.fit()
print(results_sm.summary())

# %%
# 4. Random forest
optimize_param(X_train, y_train)

rf_regressor = RandomForestRegressor(n_estimators=500,oob_score=True,n_jobs=-1,
                                  random_state=42,max_features='auto')
rf_regressor.fit(X_train,y_train)
pred_y = rf_regressor.predict(X_test)
fig, ax = plt.subplots()
ax.scatter(y_test, pred_y)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
rf_regressor.score(X_test,y_test)

# %%
#5. split the dataset into two and look for the features that differs most between the two groups
listings_low = listings[listings['availability'] < 0.5]
listings_high = listings[listings['availability'] >= 0.5]

# for dummy features use fisher_exact test
dummy_cols = listings.select_dtypes(include=['uint8', 'bool']).columns
numeric_cols = listings.drop(['id', 'availability'], axis=1).select_dtypes(include=['int', 'float']).columns
dummy_pval_high = fisher_test(listings_high, listings_low, columns=dummy_cols, alternative='greater')
dummy_pval_low = fisher_test(listings_high, listings_low, columns=dummy_cols, alternative='less')
numeric_pval_high = mannwhitneyu_test(listings_high, listings_low, columns=numeric_cols, alternative='greater')
numeric_pval_low = mannwhitneyu_test(listings_high, listings_low, columns=numeric_cols, alternative='less')

print(dummy_pval_high.sort_values())
print('')
print(dummy_pval_low.sort_values())
print('')
print(numeric_pval_high.sort_values())
print('')
print(numeric_pval_low.sort_values())

# %%
