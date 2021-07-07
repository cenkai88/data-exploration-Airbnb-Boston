## Exploratory Data Analysis on Airbnb Availability in Boston
This project is a tiny Python script that analyze the availability of Airbnb data bewteen 2016-09-06 and 2017-09-05. 

### Motivation:
As we know, economy is all about supply and demand, and the market volumn is changed by price. Since most researches on Airbnb dataset are attampts to predict prices of house, this project aims to explore:
- is there any relationship between Airbnb house price and availability
- is it possible to have a model to predict the availability using the information in Airbnb dataset
- what are the biggest differences between vacancy houses and hot ones

-----------

### Files:
- dataset: the original dataset from Kaggle
- images: images generated in the analysis
- steps: functions involved in the data analysis flow
- utils: help functions that are leveraged by the main analysis steps
- main.py: the enterence script, you can run 
  ```
  python main.py
  ```
  to check the result

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
![exploration](https://github.com/cenkai88/data-exploration-Airbnb-Boston/blob/main/images/explore-log.jpg?raw=true)

- We got a model predicting Airbnb availability with score of 0.42 using random forest regression.
![model](https://github.com/cenkai88/data-exploration-Airbnb-Boston/blob/main/images/model.jpg?raw=true)

- Using hypothesis test method, some factors are significantly different between highly available groups and less available, such as text length of house rules and the cancellation policy.

  - columns higher in vacancy houses
    | column  | pvalue  |
    |  ----  | ----  |
    |cancellation_policy_super_strict_30  |  6.772741e-23 |
    |host_about                            | 3.099518e-18 |
    |host_response_time_within an hour     | 9.874845e-15 |
    |property_type_House                   | 1.636632e-13 |
    |neighbourhood_cleansed_Dorchester     | 1.476822e-12 |
    |access                                | 3.705482e-11 |
    |cancellation_policy_strict            | 1.113465e-10 |
    |notes                                 | 8.246343e-10 |
    |require_guest_phone_verification      | 1.410842e-07 |
    |amenities_Free_Parking_on_Premises    | 1.962251e-07 |
    |host_response_rate_MEDIUM             | 2.916042e-07 |
    |house_rules_LONG                      | 3.471529e-07 |

    | column  | pvalue  |
    |  ----  | ----  |
    |number_of_reviews                 |6.170712e-48|
    |host_listings_count               |1.823288e-33|
    |calculated_host_listings_count    |2.323009e-28|
    |host_since                        |2.839037e-28|
    |reviews_per_month                 |2.128551e-13|
    |extra_people                      |2.664102e-09|
    |cleaning_fee                      |1.657983e-07|
    |security_deposit                  |4.120300e-07|

    -----------

  - columns higher in popular houses
    | column  | pvalue  |
    |  ----  | ----  |
    |amenities_Essentials                   |7.085486e-20|
    |cancellation_policy_flexible           |1.170772e-17|
    |amenities_Elevator_in_Building         |9.540255e-17|
    |neighbourhood_cleansed_Fenway          |7.958874e-09|
    |amenities_Buzzer/Wireless_Intercom     |1.013454e-08|
    |amenities_Gym                          |2.871454e-08|
    |amenities_Doorman                      |3.468097e-08|
    |host_acceptance_rate_MEDIUM            |4.239317e-07|
    |property_type_Apartment                |1.352221e-06|
    |is_location_exact                      |1.539346e-06|
    |host_response_rate_HIGH                |2.817380e-06|
    |neighbourhood_cleansed_Allston         |8.580511e-06|

    | column  | pvalue  |
    |  ----  | ----  |
    |review_scores_value          |9.778207e-16|
    |zipcode_median_price         |2.324438e-08|
    |review_scores_rating         |1.563148e-07|
    |review_scores_accuracy       |1.723554e-07|


For more info, please refer to the [Medium article](https://medium.com/p/500fb4b401c5).

-----------

### References:
- https://medium.datadriveninvestor.com/exploratory-data-analysis-on-airbnb-properties-in-paris-bce61bd680c8
- https://leo-you.github.io/Airbnb-Availability-Prediction/