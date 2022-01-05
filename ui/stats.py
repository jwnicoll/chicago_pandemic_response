import pandas as pd

def make_df(data, name):
    '''
    Given list of tuples with zip codes and quantifiers,
    convert to a series object

    Inputs:
        data: list of tuples with zip codes and quantifiers
        name: variable name

    Returns:
        Pandas series object
    '''
    dic = {}
    for datum in data:
        dic[datum[0]] = datum[1]
    series = pd.Series(dic, name=name)
    return series