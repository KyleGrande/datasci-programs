"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:

"""
import pandas as pd
import numpy as np
import numpy.linalg as LA

def import_data(file_name):
    '''
    This function has one input:
    file_name: the name of a .xls file from State-to-State Migration Flows from the US Census.
    The function reads in the file (hint: use pd.read_excel) and returns
    a DataFrame with 51 rows: the first row for United States, as well as a
    row for each state, as well as the District of Columbia.
    The columns of the DataFrame should be arranged as:
    All null values should be filled with 0.
    The first column should be named Locale and contains the name of the area.
    The first row should be United States, followed by the states in alphabetical order:
    Alabama, Alaska, ..., Wymoning (following the order in the initial datasets).
    Note that we're leaving off Puerto Rico and the US Territories since they are not
    counted in the overall estimates.
    The second column should be named Total and contains the total population for each row.
    The third column, Stayed contains the sum of the those who stayed in the same house and
    ame state (i.e. the sum of two columns from the initial excel file).
    The subsequent columns contain the number of new residents to the state,
    by previous location. For example, the third column, Alabama contains the number of
    new residents to Alabama from each state. For the row Alabama, this cell
    (e.g. df.loc['Alabama','Alabama']) would be 0, since it's the same state.
    For the row Alaska, this cell, (e.g. df.loc['Alabama','Alaska']),
    would be the number of people who moved from Alaska to Alabama this past year.
    In the case of 2019 data, there were 1,105 people who previously lived in
    Alaska and moved to Alabama.
    The row, United States2, has the total number of people for its first column,
    the number of people who didn't move, followed by the total who moved into each state.
    All other columns, such as totals, territorial information,
    and repetitions of the row labels, should be dropped.
    The resulting DataFrame should have 52 rows and 54 columns.
    This function returns a DataFrame.
    '''
    df = pd.read_excel(file_name, skiprows=7, skipfooter=11, usecols="A:DQ")

    df = df.fillna(0)

    df = df[df.iloc[:, 0] != 0].reset_index(drop=True)

    df = df.drop(index=28).reset_index(drop=True)

    df = df.loc[:, ~df.columns.str.contains("MOE")]


    df['Estimate.1'] = df['Estimate.1'].astype(int)
    df['Estimate.2'] = df['Estimate.2'].astype(int)
    df['Estimate.1'] = df['Estimate.1'] + df['Estimate.2']

    df.rename(columns={'Unnamed: 0': 'Locale', 'Estimate': 'Total',
                        'Estimate.1': 'Stayed'}, inplace=True)
    df = df.loc[:, ~df.columns.str.contains("Unnamed:")]
    df.drop(df.columns[3:5], axis=1, inplace=True)

    names = df.iloc[1:52, 0].tolist()
    df.columns = ['Locale', 'Total', 'Stayed'] + names
    df[names] = df[names].astype(int)

    return df

def make_transition_mx(df):
    '''
    This function has one input:
    df: a DataFrame with columns, Locale, Total, Stayed, followed by states' data.
    The first row (for locale United States2) is ignored and the subsequent rows
    should contain the states in the same order as the column labels.
    Returns a transition matrix, where values range from 0 to 1,
    and each column sums to 1. The entries represent the fraction of the population
    that migrated to that state, with the diagonals being the population that stayed
    (didn't move).
    '''
    transition_matrix = df.iloc[1:, 3:].div(df['Total'][1:], axis=0)
    transition_matrix = transition_matrix.fillna(0)
    transition_matrix.columns = df.columns[3:]
    transition_matrix.index = df['Locale'][1:]

    stayed_proportions = (df['Stayed'][1:] / df['Total'][1:]).to_numpy()
    np.fill_diagonal(transition_matrix.values, stayed_proportions)

    return transition_matrix.to_numpy()

def moving(transition_mx, starting_pop, num_years = 1):
    '''
    This function has three inputs and returns an array:
    transition_mx: an square array of values between 0 and 1. Each column sums to 1.
    starting_pop: an 1D array of positive numeric values that has the same length
    as transition_mx.
    num_years: a column name containing the dependent variable (what's being predicted)
    in the model. It has a default value is 1.
    The function returns an array of the population of each state after num_years.
    '''
    pop_num_years = starting_pop
    for _ in range(num_years):
        pop_num_years = transition_mx.dot(pop_num_years)
    return pop_num_years

def steady_state(transition_mx, starting_pop):
    '''
    This function has two inputs and returns an array:
    transition_mx: an square array of values between 0 and 1. Each row sums to 1.
    starting_pop: an 1D array of positive numeric values that has the same
    length as transition_mx.
    num_years: a column name containing the dependent variable (what's being predicted)
    in the model. It has a default value is 1.
    The function returns an array of the population of each state at the steady state.
    That is, it returns the eigenvector corresponding to the largest eigenvalue,
    scaled so that it's entries sum to 1, and then multiplied by the sum of
    the starting populations.
    '''
    eigen_value, eigen_vector = LA.eig(transition_mx)

    steady_state_vector = eigen_vector[:, np.isclose(eigen_value, 1)]

    steady_state_vector /= np.sum(steady_state_vector)

    total_pop = np.sum(starting_pop)

    steady_state_pop = steady_state_vector * total_pop

    return steady_state_pop.reshape(-1)
