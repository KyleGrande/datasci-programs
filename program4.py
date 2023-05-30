"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:
            pandas.Timestamp
            pandas.DataFrame.dropna
            pandas.DataFrame.fillna
            pandas.isna
            https://docs.python.org/3/library/datetime.html
            https://www.w3schools.com/python/ref_string_endswith.asp
            https://www.geeksforgeeks.org/python-string-isdigit-method/
            https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-strings/cheatsheet
"""
import pandas as pd
def make_dog_df(license_file, zipcode_file):
    '''
    This function takes two inputs:
    license_file: the name of a CSV file containing NYC Dog Licensing Data from OpenData NYC, and
    zipcode_file: the name of a CSV file containing BetaNYC's NYC Zip Codes by Borough.
    The function opens the two inputted files, the first with the dog licensing information,
    and the second with zipcodes by boroughs. The function should do the following:
    The names of the dogs AnimalName should be capitalized.
    The columns, 'LicenseExpiredDate', 'Extract Year' should be dropped.
    The two DataFrames should be (left) merged on zipcodes.
    Any reported dogs not in NYC (i.e. have NaN for Borough in the combined DataFrame)
    should be dropped.
    The resulting DataFrame, with 7 columns, is returned.
    '''
    df_license_file = pd.read_csv(license_file)
    df_zipcode_file = pd.read_csv(zipcode_file)
    df_zipcode_file = df_zipcode_file[['zip', 'borough']]
    df_license_file['AnimalName'] = df_license_file['AnimalName'].str.capitalize()
    df_license_file.drop(['LicenseExpiredDate','Extract Year'],axis=1,inplace=True)
    merged_df = pd.merge(df_license_file, df_zipcode_file, how='left',
                          left_on='ZipCode', right_on='zip')
    merged_df.drop(['zip'], axis=1, inplace=True)
    merged_df = merged_df.dropna(subset=['borough'])
    merged_df.rename(columns={'borough': 'Borough'},
              inplace=True)
    return merged_df
def make_bite_df(file_name):
    '''
    This function takes one input:
    file_name: the name of a CSV file containing DOHMH Dog Bite Data from OpenData NYC.
    The function should open the file file_name as DataFrame, dropping the Species column.
    The resulting DataFrame is returned.
    '''
    df = pd.read_csv(file_name)
    df.drop(['Species'], axis=1, inplace=True)
    return df
def clean_age(age_str):
    '''
    This function takes one input:
    age_str: a string containing the age of the dog.
    Your function should:
    If age_str ends in a Y, return the rest of the string as a number. For example,
    3Y represents 3 years and the return value is 3.
    If age_str ends in a M, return the rest of the string as a number in years.
    For example, 6M represents 6 months and the return value is 0.5.
    If age_str contains only a number, return it as a number. For example,
    3 represents 3 years and the return value is 3.
    For all other values, return None.
    '''
    age_str = str(age_str)
    if age_str.endswith('Y'):
        return float(age_str[:-1])
    if age_str.endswith('M'):
        return float(age_str[:-1])/12
    if age_str.isdigit():
        return float(age_str)
    return None
def clean_breed(breed_str):
    '''
    This function takes one input:
    breed_str: a string containing the breed of the dog.
    Your function should return:
    If breed_str is empty, return "Unknown".
    Otherwise, return the string in title format with each word in the string capitalized
    and all other letters lower case. For example, If the input is BEAGLE MIXED,
    you should return Beagle Mixed.
    '''
    if breed_str is None:
        return 'Unkown'
    return breed_str.title()
def impute_age(df):
    '''
    This function takes one input:
    df: a DataFrame containing the column Age Num.
    Your function should replace any missing values in the df['Age Num']
    column with the median of the values of the column. The resulting DataFrame is returned.
    '''
    median = df['Age Num'].median()
    df['Age Num'] = df['Age Num'].fillna(median)
    return df
def impute_zip(boro, zipcode):
    '''
    This function takes two inputs:
    boro: a non-empty string containing the borough.
    zipcode: a possibly empty string containing the zip code.
    If the zipcode column is empty, impute the value with the zip code of the
    general delivery post office based on value of boro:
    10451 for Bronx, 11201 for Brooklyn, 10001 for Manhattan,
    11431 for Queens, 10341 for Staten Island,
    and None for Other.
    '''
    if pd.isna(zipcode):
        if boro == 'Bronx':
            zipcode= 10451
        elif boro == 'Brooklyn':
            zipcode= 11201
        elif boro == 'Manhattan':
            zipcode= 10001
        elif boro == 'Queens':
            zipcode= 11431
        elif boro == 'Staten Island':
            zipcode= 10341
        else:
            zipcode= None
        return zipcode
    return zipcode
def parse_datetime(df, column='LicenseIssuedDate'):
    '''
    This function takes two inputs:
    df: a DataFrame containing the column column. column has a default value of 'LicenseIssuedDate'
    The function should return a DataFrame with three additional columns:
    timestamp: contains the datetime object corresponding to the string stored in column.
    month: return the number corresponding to the month of timestamp:
    1 for January, 2 for February, ... 12 for December.
    day_of_week: return the number corresponding to the day of the week of timestamp:
    0 for Monday, 1 for Tuesday, ... 6 for Sunday.
    '''
    df['timestamp'] = pd.to_datetime(df[column])
    df['month'] = df['timestamp'].dt.month
    df['day_of_week'] = df['timestamp'].dt.weekday
    return df
