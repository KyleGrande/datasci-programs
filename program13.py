"""
Name: Kyle Grande
Email: kyle.grande72@myhunter.cuny.edu
Resources:
        pandasql docs: https://pypi.org/project/pandasql/
"""
import pandas as pd
import pandasql as ps


def make_df(file_name):
    '''
    Reads a csv file and returns a dataframe
    :param file_name: name of the csv file
    :return: dataframe
    '''

    df = pd.read_csv(file_name)
    return df

def count_null_repositories(df):
    '''
    counts the number of null repositories
    :param df: dataframe
    :return: dataframe with the number of null repositories
    '''

    query = """
    SELECT COUNT(*) as num_repos
    FROM df
    WHERE repository_url IS NULL
    """

    result = ps.sqldf(query, locals())
    return result

def count_repos_by_language(df):
    '''
    counts the number of repositories by language
    :param df: dataframe
    :return: dataframe with the number of repositories by language
    '''

    query = """
    SELECT language, COUNT(*) as num_repos
    FROM df
    WHERE language IS NOT NULL
    GROUP BY language
    ORDER BY language
    """

    result = ps.sqldf(query, locals())
    return result

def count_ml_repos(df):
    '''
    counts the number of repositories that contain the phrase 'machine learning'
    :param df: dataframe
    :return: dataframe with the number of repositories that contain the phrase 'machine learning'
    '''

    query = """
    SELECT COUNT(*) as num_repos
    FROM df
    WHERE keywords LIKE '%machine learning%'
    """

    result = ps.sqldf(query, locals())
    return result

def find_most_recent_timestamp(df):
    '''
    finds the most recent timestamp
    :param df: dataframe
    :return: dataframe with the most recent timestamp
    '''

    query = """
    SELECT MAX(created_timestamp) as most_recent_timestamp
    FROM df
    """

    result = ps.sqldf(query, locals())
    return result

def count_python_repo_with_missing_license(df):
    '''
    counts the number of python repositories with missing license
    :param df: dataframe
    :return: dataframe with the number of python repositories with missing license
    '''

    query = """
    SELECT COUNT(*) as num_go_repo_with_missing_license
    FROM df
    WHERE language = 'Python' AND licenses IS NULL
    """

    result = ps.sqldf(query, locals())
    return result
