import pandas as pd

from utils.formatter import calendar_updated_formatter
from utils.clean_helper import drop_nas, generate_dummies, convert_to_bool, convert_to_num, fill_col_na, process_zipcode, process_amenities

def clean_listings_data(listings):
  '''
    INPUT
    df - the original dataframe

    OUTPUT
    the cleaned df
  '''
  listings = listings.dropna(axis=1, how='all')

  columns_to_drop = [
    # ids are not needed
    'scrape_id',
    'host_id',
    # only one unique value
    'last_scraped',
    'experiences_offered',
    'state',
    'country_code',
    'country',
    'calendar_last_scraped',
    'requires_license',
    # urls are not needed
    'medium_url',
    'listing_url',
    'thumbnail_url',
    'picture_url',
    'xl_picture_url',
    'host_url',
    'host_thumbnail_url',
    'host_picture_url',
    # long texts without fixed keywords which is too complex to analyze for this project
    'name',
    'host_name',
    'description',
    'summary',
    'space',
    'interaction',
    # will use zipcode for location
    'street',
    'neighbourhood',
    'city', 
    'market',
    'smart_location',
    'latitude',
    'longitude',
    # not important for analysis
    'host_location',
    'host_verifications',
    'first_review',
    # use price as the only price indicator
    'weekly_price',
    'monthly_price',
    # use availability_365 as the only availability indicator
    'availability_30',
    'availability_60',
    'availability_90',
    # duplicated
    'host_total_listings_count',
    # use neighbourhood_cleansed instead
    'host_neighbourhood',
    # very few valid data and square_feet should have a strong relationship with room number
    'square_feet'
  ]

  listings = drop_nas(listings, columns_to_drop)

  # convert value to boolean
  columns_to_bool = [
    ['neighborhood_overview', False],
    ['notes', False],
    ['transit', False],
    ['access', False],
    ['host_about', False],
    ['host_is_superhost', 't'],
    ['host_has_profile_pic', 't'],
    ['host_identity_verified', 't'],
    ['is_location_exact', 't'],
    ['instant_bookable', 't'],
    ['require_guest_profile_picture', 't'],
    ['require_guest_phone_verification', 't'],
  ]

  listings = convert_to_bool(listings, columns_to_bool)
   
  # convert to number by stripping unnecessary stirngs including '$' and '%'
  columns_to_num = [
    ['host_since', 'DATERANGE'],
    ['last_review', 'DATERANGE'],
    ['cleaning_fee', 'CURRENCY'],
    ['extra_people', 'CURRENCY'],
    ['security_deposit', 'CURRENCY'],
    ['price', 'CURRENCY'],
    ['host_response_rate', 'PERCENT'],
    ['host_acceptance_rate', 'PERCENT'],
    ['house_rules', 'TEXTLENGTH'],
  ]
  listings = convert_to_num(listings, columns_to_num)

  listings['availability'] = listings['availability_365'] / 365
  listings.drop(['availability_365'], axis=1, inplace=True)
  listings[['price']] = listings[['price']].astype('float64')

  # convert to category (since some of the numeric values are not evenly distributed, we need to convert them into categories)

  listings['house_rules'] = listings['house_rules'].apply(
      lambda x: 'LONG' if x > 246 else ('MEDIUM' if x > 71 else 'SHORT'))

  listings['host_response_rate'] = listings['host_response_rate'].apply(
      lambda x: 'HIGH' if x > 0.97 else ('MEDIUM' if x > 0.8 else 'LOW'))

  listings['host_acceptance_rate'] = listings['host_acceptance_rate'].apply(
      lambda x: 'HIGH' if x > 0.94 else ('MEDIUM' if x > 0.71 else 'LOW'))

  listings['calendar_updated'] = listings['calendar_updated'].apply(
      calendar_updated_formatter)

  # fillin na:
  # mean(review scores), 
  # 1(rooms), 
  # 0(reviews per month when there's no review), 
  # mode(host response time)

  columns_to_fill_na = [
    ['review_scores_rating', listings['review_scores_rating'].mean()],
    ['review_scores_accuracy', listings['review_scores_accuracy'].mean()],
    ['review_scores_cleanliness', listings['review_scores_cleanliness'].mean()],
    ['review_scores_checkin', listings['review_scores_checkin'].mean()],
    ['review_scores_communication', listings['review_scores_communication'].mean()],
    ['review_scores_value', listings['review_scores_value'].mean()],
    ['review_scores_location', listings['review_scores_location'].mean()],
    ['reviews_per_month', 0],
    ['bathrooms', 1],
    ['bedrooms', 1],
    ['beds', 1],
    ['host_response_time', listings['host_response_time'].mode()]
  ]

  listings = fill_col_na(listings, columns_to_fill_na)

  # %%
  # clean zipcode and create a zipcode_median_price:
  # Used zipcode to represent the location of property, 
  # and calculated the median price (since there are outliners for price) for each zipcode(area) 
  # and try to normalize the price of each property to get rid of the location factor.
  listings = process_zipcode(listings)

  # %%
  # convert amenities column since its original format is not flat
  listings = process_amenities(listings)

  # %%
  # wrap up and generate dummy columns
  listings = generate_dummies(listings)
  return listings