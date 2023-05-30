"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:  pandas.pydata.org for:
                                pandas.DataFrame
                                pandas.DataFrame.merge
                                pandas.DataFrame.filter
                                pandas.DataFrame.mean
"""
import pandas as pd

def clean_df(df, year=2015):
    '''
    clean_df(df, year = 2015): This function takes two inputs:
    df: the name of a DataFrame containing TreesCount Data from OpenData NYC.
    year: the year of the data set. There are three possible years 1995, 2005, or 2015.
    Drops all columns except given ones, and renames older verisons to match 2015
    '''
    if year == 2015:
        df = df.loc[:, ['tree_dbh',
                        'health',
                        'spc_latin',
                        'spc_common',
                        'nta',
                        'latitude',
                        'longitude',
                        ]]

    elif year == 2005:
        df = df.loc[:, ['tree_dbh',
                        'status',
                        'spc_latin',
                        'spc_common',
                        'nta',
                        'latitude',
                        'longitude',
                        ]]
        df.rename(columns={'status': 'health'},
                  inplace=True)

    elif year == 1995:
        df = df.loc[:, ['diameter',
                        'condition',
                        'spc_latin',
                        'spc_common',
                        'nta_2010',
                        'latitude',
                        'longitude',
                        ]]
        df.rename(columns={'diameter': 'tree_dbh',
                           'condition': 'health',
                           'nta_2010': 'nta'},
                  inplace=True)
    return df

def make_nta_df(file_name):
    '''
    make_nta_df(file_name): This function takes one input:
    file_name: the name of a CSV file containing population and names
    for neighborhood tabulation areas (NYC OpenData NTA Demographics).
    The function should open the file file_name as DataFrame, returns
    a DataFrame containing only the columns containing the NTA code
    (labeled as nta_code), the neigborhood name (labeled as nta_name),
    and the 2010 population (labeled as population).
    '''
    df = pd.read_csv(file_name)
    column_names = df.filter(regex='(NTA)|(Population 2010)').columns.tolist()
    df = df[column_names]
    df.rename(columns={df.columns[0]: 'nta_code',
                       df.columns[1]: 'nta_name',
                       df.columns[2]: 'population'},
              inplace=True)
    df = df.dropna()
    return df


def count_by_area(df):
    '''
    count_by_area(df): This function takes one inputs:
    df: a DataFrame that includes the nta column.
    The function should return a DataFrame that has two columns, [nta, num_trees]
    where nta is the code of the Neighborhood Tabulation Area and num_trees is the
    sum of the number of trees, grouped by nta.

    Hint: count_by_area is similar to the one written in Program 2, but a DataFrame
    (not a groupby object) is expected. See Chapter 6.2 on aggregating, resetting
    indices, and converting groupby objects into DataFrames.
    '''
    df = df.groupby('nta').size().reset_index(name='num_trees')
    return df


def neighborhood_trees(tree_df, nta_df):
    '''
    This function takes two inputs:
    tree_df: a DataFrame containing the column nta
    nta_df: a DataFrame with two columns, 'NTACode' and 'NTAName'.
    This function returns a DataFrame as a result of joining the two
    input dataframes, with tree_df as the left table. The join should be on NTA code.
    The resulting dataframe should contain the following columns, in the following order:
    nta
    num_trees
    nta_name
    population
    trees_per_capita: this is a newly calculated column, calculated by dividing the number
    of trees by the population in each neighborhood.
    '''
    df = tree_df.merge(nta_df, left_on='nta', right_on='nta_code')
    # df = pd.merge(tree_df, nta_df, left_on='nta', right_on='nta_code')
    # tree_df.drop('nta_code', inplace=True)
    df['trees_per_capita'] = df['num_trees'] / df['population']
    df = df[['nta', 'num_trees', 'nta_name', 'population', 'trees_per_capita']]
    return df


def compute_summary_stats(df, col):
    '''
    This function takes two inputs:
    df: a DataFrame containing a column col.
    col: the name of a numeric-valued col in the DataFrame.
    This function returns the mean and median of the Series df[col].
    Note that since numpy is not one of the libraries for this assignment,
    your function should compute these statistics without using numpy.
    '''
    # mean = sum(df[col])/len(df[col])
    mean = df[col].mean()
    median = df[col].median()
    return mean, median


def mse_loss(theta, y_vals):
    '''
    This function takes two inputs::
    theta: a numeric value.
    y_vals: a Series containing numeric values.
    Computes the Mean Squared Error of the parameter theta and a Series,
    y_vals. See Section 4.2: Modeling Loss Functions where this function
    is implemented using numpy. Note that numpy is not one of the libraries for
    this assignment and your function should compute MSE without using numpy.
    '''
    mean_squared_error = (((y_vals - theta) ** 2).sum()) / len(y_vals)
    return mean_squared_error


def mae_loss(theta, y_vals):
    '''
    This function takes two inputs:
    theta: a numeric value.
    y_vals: a Series containing numeric values.
    Computes the Mean Absolute Error of the parameter theta and a Series,
    y_vals. See Section 4.2: Modeling Loss Functions where this function is
    implemented using numpy. Note that numpy is not one of the libraries for
    this assignment and your function should compute MAE without using numpy.
    '''
    mean_absolute_error = ((abs(y_vals - theta)).sum()) / len(y_vals)
    return mean_absolute_error


def test_mse(loss_fnc=mse_loss):
    '''
    This test function takes one input:
    loss_fnc: a function that takes in two input parameters (a numeric
    value and a Series of numeric values) and returns a numeric value.
    It has a default value of mse_loss. This is a test function, used to
    test whether the loss_fnc returning True if the loss_fnc performs correctly
    (e.g. computes Mean Squared Error) and False otherwise.
    '''
    y_vals = pd.Series([1, 2, 3, 4, 5])
    z_vals = pd.Series([6, 7, 8, 9, 10])
    if loss_fnc(1, y_vals) == mse_loss(1, y_vals):
        if loss_fnc(1, z_vals) == mse_loss(1, z_vals):
            return True
    return False
