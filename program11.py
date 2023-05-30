"""
Name: Kyle Grande
Email: kyle.grande72@myhunter.cuny.edu
Resources:
    Chapter 13
    Classwork 9
"""

import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
# from datetime import datetime

def make_df(file_name):
    '''
    make_df(file_name): This function takes one input:

    file_name:
        the name of a CSV file containing 911 System Calls from OpenData NYC.

    The data is read into a DataFrame.
    Rows that are have null values for the type description,
    incident date, incident time, latitute and longitude are dropped.
    Only rows that contain AMBULANCE as part of the TYP_DESC are kept.
    The resulting DataFrame is returned.
    Hint: see DS 100: Chapter 13 for using string methods within pandas.
    See Classwork 9.
    '''
    df = pd.read_csv(file_name)
    df.dropna(subset=['TYP_DESC', 'INCIDENT_DATE', 'INCIDENT_TIME', 'Latitude', 'Longitude'], inplace=True)
    df = df[df['TYP_DESC'].str.contains('AMBULANCE')]
    return df

def add_date_time_features(df):
    '''
    add_date_time_features(df): This function takes one input:

    df: a DataFrame containing 911 System Calls from OpenData NYC created by make_df.

    An additional column WEEK_DAY is added with the day of the week (0 for Monday,
    1 for Tuesday, ..., 6 for Sunday) of the date in INCIDENT_DATE is added.
    Another column, INCIDENT_MIN, that takes the time from INCIDENT_TIME
    and stores it as the number of minutes since midnight.
    The resulting DataFrame is returned.
    Hint: see Lecture 3 for using datetime methods with pandas,
    including computing the day of the week (of datetime objects)
    and the total seconds (of timedelta objects).
    '''
    df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'])
    df['WEEK_DAY'] = df['INCIDENT_DATE'].dt.weekday
    df['INCIDENT_TIME'] = pd.to_datetime(df['INCIDENT_TIME'], format='%H:%M:%S').dt.time
    df['INCIDENT_MIN'] = df['INCIDENT_TIME'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
    return df


def filter_by_time(df, days=None, start_min=0, end_min=1439):
    '''
    filter_by_time(df, days=None, start_min=0, end_min=1439):
    This function takes four inputs:

    df: a DataFrame containing 911 System Calls from OpenData NYC.

    days: a list of integers ranging from 0 to 6, representing the days of the week.
    The default value is None and is equivalent to the list containing all days:
    [0,1,2,3,4,5,6].

    start_min: a non-negative integer value representing the starting time.
    With end_min, it representing the range, inclusive, for the time, in minutes,
    that should be selected. The default value give the range of [0,1439] which
    ranges from midnight (0 minutes) to (1439 representing 23:59 since
    23 hours + 59 minutes = 23*60+59 minutes = 1439 minutes).

    end_min: a non-negative integer value representing the ending time.
    With start_min, it representing the range, inclusive, for the time,
    in minutes, that should be selected. The default value give the range of
    [0,1439] which ranges from midnight (0 minutes) to (1439 representing
    23:59 since 23 hours + 59 minutes = 23*60+59 minutes = 1439 minutes).

    Returns a DataFrame with entries restricted to weekdays in days
    (or all weekdays if None is given) and incident times in [start_min, end_min]
    inclusive (e.g. contains the endpoints).

    '''
    if days is None:
        days = [0, 1, 2, 3, 4, 5, 6]
    df = df[df['WEEK_DAY'].isin(days) & (df['INCIDENT_MIN'] >= start_min) & (df['INCIDENT_MIN'] <= end_min)]
    return df


def compute_kmeans(df, num_clusters=8, n_init='auto', random_state=2022):
    '''
    compute_kmeans(df, num_clusters = 8, n_init = 'auto', random_state = 2022):
    This function takes four inputs:
    df: a DataFrame containing 911 System Calls from OpenData NYC.

    n_init: Number of times the k-means algorithm is run with different centroid seeds.
    The final results is the best output of n_init consecutive runs in terms of inertia.
    The default value is auto.

    num_clusters: an integer representing the number of clusters.
    The default value is 8.

    random_state: the random seed used for KMeans. The default value is 2022.

    Runs the KMeans model with num_clusters on the latitude and longitude data
    of the provided DataFrame. Returns the cluster centers and predicted labels
    computed via the model.
    A similar, but not identical function was part of Classwork 9.
    '''
    model = KMeans(n_clusters=num_clusters, n_init=n_init, random_state=random_state)
    model.fit(df[['Latitude', 'Longitude']])
    return model.cluster_centers_, model.labels_

def compute_gmm(df, num_clusters=8, random_state=2022):
    '''
    compute_gmm(df, num_clusters = 8, random_state = 2022):
    This function takes three inputs:

    df: a DataFrame containing 911 System Calls from OpenData NYC.

    num_clusters: an integer representing the number of clusters. The default value is 8.

    random_state: the random seed used for GaussianMixture. The default value is 2022.

    Runs the GaussianMixture model with num_clusters on the latitude and longitude
    Data of the provided DataFrame.
    Returns the array of the predicted labels computed via the model.
    '''
    model = GaussianMixture(n_components=num_clusters, random_state=random_state)
    model.fit(df[['Latitude', 'Longitude']])
    model_gnm = model.predict(df[['Latitude', 'Longitude']])
    return model_gnm


def compute_agglom(df, num_clusters=8, linkage='ward'):
    '''
    compute_agglom(df, num_clusters = 8, linkage='ward'):
    This function takes three inputs:
    df: a DataFrame containing 911 System Calls from OpenData NYC.

    num_clusters: an integer representing the number of clusters.
    The default value is 8.

    linkage: the linkage criterion used determining distances between sets for
    AgglomerativeClustering. The default value is 'ward'.
    Runs the Agglomerative model with num_clusters on the latitude and longitude
    data of the provided DataFrame and default linkage (i.e. ward).

    Returns the array of the predicted labels computed via the model.
    '''
    model = AgglomerativeClustering(n_clusters=num_clusters, linkage=linkage)
    model.fit(df[['Latitude', 'Longitude']])
    return model.labels_

def compute_explained_variance(df, K=[1, 2, 3, 4, 5], random_state=55):
    '''
    compute_explained_variance(df, K =[1,2,3,4,5], random_state = 55):
    This function takes three inputs:

    df: a DataFrame containing 911 System Calls from OpenData NYC.

    K: a list of integers representing values for the number of clusters.
    The default value is [1,2,3,4,5].

    random_state: the random seed used for KMeans. The default value is 55.

    Returns a list of the sum of squared distances of samples to their
    closest cluster center for each value of K.
    This can be computed manually or via the inertia_ attribute of the KMeans model.
    '''
    explained_variance = []
    for k in K:
        model = KMeans(n_clusters=k, random_state=random_state)
        model.fit(df[['Latitude', 'Longitude']])
        explained_variance.append(model.inertia_)
    return explained_variance

# def main():
#     df = make_df('NYPD_Calls_Manhattan_4Jul2021.csv')
#     print(df[['INCIDENT_TIME','TYP_DESC','Latitude','Longitude']])
#     df = add_date_time_features(df)
#     print(df[['INCIDENT_DATE','WEEK_DAY','INCIDENT_TIME','INCIDENT_MIN']])
#     df_early_am = filter_by_time(df, times=[(0, 359)])
#     print(df_early_am[['INCIDENT_DATE','WEEK_DAY','INCIDENT_TIME','INCIDENT_MIN']])
# if __name__ == '__main__':
#     main()