import pandas as pd
import numpy as np


class DatasetConsumption:
    def __init__(self, dataset:pd.DataFrame):
        self.df = dataset

    def get_transformed_dataset(self)->pd.DataFrame:
        """
        Get a transformed data from the original one with the following columns:
        country String representing a given country
        average_outstanding Average amount of pending transactions per country
        total_completed Total amount of completed transactions per country
        critical_rate Error rate (failed transactions over the total number of transactions) with an amount greater than $1M per country
        error_rate Error rate (failed transactions over the total number of transactions) with an amount smaller or equal than $1Mper country

            args: None
            return: pandas.DataFrame()
        
        """
        df_t = self.df.copy()
        df_t.dropna(inplace=True)
        N = len(df_t)
        #Create dummy columns to compute new statistics
        df_t['average_outstanding'] = df_t.apply(lambda x: 1 if x['status'] == 'PENDING' else 0, axis=1)
        df_t['total_completed'] = df_t.apply(lambda x: 1 if x['status'] == 'COMPLETED' else 0, axis=1)
        df_t['critical_rate'] = df_t.apply(lambda x: 1 if x['status'] == 'FAILED' and x['amount'] > 1e6 else 0, axis=1)
        df_t['error_rate'] = df_t.apply(lambda x: 1 if x['status'] == 'FAILED' and x['amount'] <= 1e6 else 0, axis=1)

        group_col = ['country']
        non_group_col = ['average_outstanding', 'total_completed', 'critical_rate', 'error_rate']

        #df_t = df_t.groupby(group_col, as_index=False)[non_group_col].agg(lambda x: sum([i for i in x]))
        df_t = df_t.groupby(group_col, as_index=False)[non_group_col].sum()
        df_t['average_outstanding'] = df_t['average_outstanding'] / N
        df_t['critical_rate'] = df_t['critical_rate'] / N 
        df_t['error_rate'] = df_t['error_rate'] / N

        return df_t
        
    







    