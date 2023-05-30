"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:
            Lecture 4
            Lecture 6
            datetime
            Lecture 5
            Chapter 15
            pandas.DataFrame.get_dummies
            https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
            https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression
            https://docs.python.org/3/library/pickle.html
            https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
            https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
            https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
"""
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def import_data(file_name):
    '''
    This function takes as one input parameter:
    file_name: the name of a CSV file containing Yellow Taxi Trip Data from OpenData NYC.
    The data in the file is read into a DataFrame, and
    the columns: VendorID,RatecodeID,store_and_fwd_flag,payment_type,
    extra,mta_tax,tolls_amount,improvement_surcharge,congestion_surcharge are dropped.
    Any rows with non-positive total_amount are dropped.
    The resulting DataFrame is returned.
    '''
    df = pd.read_csv(file_name)
    df = df.drop(columns=['VendorID','RatecodeID','store_and_fwd_flag',
                          'payment_type','extra','mta_tax','tolls_amount',
                          'improvement_surcharge','congestion_surcharge'])
    df = df[df['total_amount'] > 0]
    return df

def add_tip_time_features(df):
    '''
    This function takes one input:
    df: a DataFrame containing Yellow Taxi Trip Data from OpenData NYC.
    The function computes 3 new columns:
    percent_tip: which is 100*tip_amount/(total_amount-tip_amount)
    duration: the time the trip took in seconds.
    dayofweek: the day of the week that the trip started,
    represented as 0 for Monday, 1 for Tuesday, ... 6 for Sunday.
    The original DataFrame with these additional three columns is returned.
    '''
    df['percent_tip'] = 100 * df['tip_amount'] / (df['total_amount'] - df['tip_amount'])
    df['duration'] = (pd.to_datetime(df['tpep_dropoff_datetime'])
                       - pd.to_datetime(df['tpep_pickup_datetime'])
                       ).dt.total_seconds()
    df['dayofweek'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.dayofweek
    return df

def impute_numeric_cols(df):
    '''
    This function takes one input:
    df: a DataFrame containing Yellow Taxi Trip Data from OpenData NYC.
    Missing data in the numeric columns passenger_count,trip_distance,
    fare_amount,tip_amount,total_amount,duration,dayofweek are
    replaced with the median of the respective column.
    Returns the resulting DataFrame.
    '''
    missing_data = ['passenger_count', 'trip_distance', 'fare_amount',
                    'tip_amount', 'total_amount', 'duration', 'dayofweek']
    df[missing_data] = df[missing_data].fillna(df[missing_data].median())

    return df

def add_boro(df, file_name) -> pd.DataFrame:
    '''
    This function takes as two input parameters:
    df: a DataFrame containing Yellow Taxi Trip Data from OpenData NYC.
    file_name: the name of a CSV file containing NYC Taxi Zones from OpenData NYC.
    Makes a DataFrame, using file_name, to add pick up and drop off boroughs to df.
    In particular, adds two new columns to the df:
    PU_borough that contain the borough corresponding
    to the pick up taxi zone ID (stored in PULocationID)
    DO_borough that contain the borough corresponding
    to the drop off taxi zone (stored in DOLocationID)
    Returns df with these two additional columns (PU_borough and DO_borough).
    '''
    df2 = pd.read_csv(file_name)
    df = pd.merge(df, df2[['LocationID', 'borough']],
            left_on='PULocationID', right_on='LocationID', how='left')
    df.rename(columns={'borough': 'PU_borough'}, inplace=True)
    df.drop(columns=['LocationID'], inplace=True)
    df = pd.merge(df, df2[['LocationID', 'borough']],
            left_on='DOLocationID', right_on='LocationID', how='left')
    df.rename(columns={'borough': 'DO_borough'}, inplace=True)
    df.drop(columns=['LocationID'], inplace=True)
    return df

def encode_categorical_col(col,prefix):
    '''
    This function takes two input parameters:
    col: a column of categorical data.
    prefix: a prefix to use for the labels of the resulting columns.
    Takes a column of categorical data and uses categorical encoding
    to create a new DataFrame with the k-1 columns, where k is the number
    of different nomial values for the column. Your function should create
    k columns, one for each value, labels by the prefix concatenated with the value.
    The columns should be sorted and the DataFrame restricted to the first k-1
    olumns returned.
    Note: we presented several different ways to categorically encode nomial data in Lecture 5.
    The book details an approach using sklearn in Chapter 15,
    and you may find Panda's get_dummies useful.
    '''
    col = pd.get_dummies(col, prefix=prefix, prefix_sep='')
    col = col.iloc[:, :-1]
    return col



def split_test_train(df, xes_col_names, y_col_name, test_size=0.25, random_state=1870):
    '''
    This function takes 5 input parameters:
    df: a DataFrame containing Yellow Taxi Trip Data from OpenData NYC
    to which add_boro() has been applied.
    y_col_name: the name of the column of the dependent variable.
    xes_col_names: a list of columns that contain the independent variables.
    test_size: accepts a float between 0 and 1 and represents the proportion of the
    data set to use for training. This parameter has a default value of 0.25.
    random_state: Used as a seed to the randomization. This parameter has a default
    value of 1870.
    Calls sklearn's train_test_split function to split the data set into a training
    and testing
    subsets: x_train, x_test, y_train, y_test. The resulting 4 subsets are returned.
    Hint: see the examples from Lecture 4 for a similar splitting of data into
    training and testing datasets.
    '''
    xes = df[xes_col_names]
    yes = df[y_col_name]
    x_train, x_test, y_train, y_test = train_test_split(xes, yes,
                test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train, y_test

def fit_linear_regression(x_train, y_train):
    '''
    This function takes two inputs:
    x_train: an array of numeric columns with no null values.
    y_train: an array of numeric columns with no null values.
    Fits a linear model to x_train and y_train, using sklearn.
    linear_model.LinearRegression (see lecture & textbook for details
    on setting up the model). The resulting model should be returned
    as bytestream,
    using pickle (see Lecture 4).
    '''
    model = LinearRegression()
    model.fit(x_train, y_train)
    mod_pkl = pickle.dumps(model)
    return mod_pkl

def predict_using_trained_model(mod_pkl, xes, yes):
    '''
    This function takes three inputs:
    mod_pkl: a trained model for the data, stored in pickle format.
    xes: an array or DataFrame of numeric columns with no null values.
    yes: an array or DataFrame of numeric columns with no null values.
    Computes and returns the mean squared error and r2 score between the
    values predicted by the model (mod_pkl on x) and the actual values (y).
    Note that sklearn.metrics contains two functions that may be of use:
    mean_squared_error and r2_score.
    '''
    model = pickle.loads(mod_pkl)
    y_predict = model.predict(xes)
    mse = mean_squared_error(yes, y_predict)
    r2_result= r2_score(yes, y_predict)
    return mse, r2_result
