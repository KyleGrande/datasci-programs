"""
    Name: Kyle Gene Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:  pandas.pydata.org for:
                                pandas.DataFrame
                                for pandas.DataFrame.rename
                                for pandas.DataFrame.isin
                                pandas.core.groupby.GroupBy.size
"""
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
                        'address',
                        'zipcode',
                        'boroname',
                        'nta',
                        'latitude',
                        'longitude',
                        'council_district',
                        'census_tract'
                        ]]

    elif year == 2005:
        df = df.loc[:, ['tree_dbh',
                    'status',
                        'spc_latin',
                        'spc_common',
                        'address',
                        'zipcode',
                        'boroname',
                        'nta',
                        'latitude',
                        'longitude',
                        'cncldist',
                        'census_tract'
                        ]]
        df.rename(columns={'status': 'health',
                           'cncldist': 'council_district'}, inplace=True)

    elif year == 1995:
        df = df.loc[:, ['diameter',
                    'condition',
                        'spc_latin',
                        'spc_common',
                        'address',
                        'zip_original',
                        'borough',
                        'nta_2010',
                        'latitude',
                        'longitude',
                        'council_district',
                        'censustract_2010'
                        ]]
        df.rename(columns={'diameter': 'tree_dbh', 'condition': 'health',
                           'zip_original': 'zipcode', 'borough': 'boroname',
                           'nta_2010': 'nta', 'censustract_2010': 'census_tract'},
                  inplace=True)

    return df


def filter_health(df, keep):
    '''
    filter_health(df, keep): This function takes two inputs:
    df: a DataFrame that includes the health column.
    keep: a list of values for the health column.
    The function returns the DataFrame with only rows that where the column
    health contains a value from the list keep. All rows where the health column
    contains a different value are dropped.
    '''
    #creates sub df from health and checks if a value in keep is in health
    df = df[df['health'].isin(keep)]
    return df

def add_indicator(row):
    '''
    add_indicator(row): This function takes one input:
    row: a Series (a row) containing values for tree_dbh and health.
    The function should return 1 if health is not Poor and tree_dbh is
    larger than 10. Otherwise, it should return 0.
    '''
    #checks given row for to see if health is poor or if diameter is greater than 10
    if (row['health'] != 'Poor') and (row['tree_dbh'] > 10):
        return 1
    return 0

def find_trees(df, species):
    '''
    find_trees(df, species): This function takes two inputs:
    df: a DataFrame that includes the spc_latin column and the address column.
    species: a string containing the Latin name of a tree.
    The function should return, as a list, the address for all trees of that species
    in spc_latin. If that species does not occur in the DataFrame, then an empty list is returned.
    '''
    lst = {}
    #creates a df of given spieces then adds the address to the list
    lst = df[df['spc_latin'] == species]['address'].tolist()
    return lst

def count_by_area(df, area="boroname"):
    '''
    count_by_area(df, area = "boroname"): This function takes two inputs:
    df: a DataFrame that includes the area column.
    area: the name of a column in df. The default value is "boroname".
    The function should return the sum of the number of trees, grouped by area.
    For example if area = "boroname", your function should group by boroname and
    return the number of each trees in each of the boroughs.
    '''
    #uses size() to get num of trees that are in group area
    df = df.groupby(area).size()
    return df
