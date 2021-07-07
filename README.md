## Exploratory Data Analysis on Airbnb Availability in Boston
This project is a tiny Python script that analyze the availability of Airbnb data bewteen 2016-09-06 and 2017-09-05. 

### Motivation:
As we know, economy is all about supply and demand, and the market volumn  is changed by price. Since most researches on Airbnb dataset are attampts to predict prices of house, this project aims to explore:
- if there is any relationship between Airbnb house price and availability
- if it possible to have a model to predict the availability using the information in Airbnb dataset
- what are the biggest differences between vacancy houses and hot ones

-----------

### Dependencies:
This repo requires:
- Python (>= 3.7)
- Conda (>=4.10.1)
  
Packages used are:
- Pandas
- Numpy
- Scipy
- Statsmodels
- Sklearn
  
-----------

### Results:
- Price has little direct correlation with availability in this dataset.


- We got a model predicting Airbnb availability with score of 0.42 using random forest regression.


- Using hypothesis test method, some factors are significantly different between highly available groups and less available, such as text length of house rules and the cancellation policy.



For more info, please refer to the [Medium article](https://medium.com/p/500fb4b401c5/edit).

-----------

### References:
- https://medium.datadriveninvestor.com/exploratory-data-analysis-on-airbnb-properties-in-paris-bce61bd680c8
- https://leo-you.github.io/Airbnb-Availability-Prediction/