import pandas as pd
import numpy as np
from argparse import ArgumentParser
import time

class DatasetConsumption:
    def __init__(self, dataset:pd.DataFrame):
        self.df = dataset

    def get_transformed_dataset(self)->pd.DataFrame:
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

        df_t = df_t.groupby(group_col, as_index=False)[non_group_col].agg(lambda x: sum([i for i in x]))
        df_t['average_outstanding'] = df_t['average_outstanding'] / N
        df_t['critical_rate'] = df_t['critical_rate'] / N 
        df_t['error_rate'] = df_t['error_rate'] / N

        return df_t
        
    

def manage_arguments():
    parser = ArgumentParser()
    parser.add_argument('--output-type',
                        help="Indicates whether the transformed dataset will be stored: 'csv', 's3' or 'postgres' ",
                        metavar='output')
    return parser.parse_args()

def main(args):
    output = args.output
    assert output == 'csv' or output == 's3' or output == 'postgres', "Output should be 'csv', 's3' or 'postgres'"
    consumer = DatasetConsumption()
    start = time.time()
    df_new = consumer.get_transformed_dataset()
    end = time.time()
    print(end - start)



if __name__ == "__main__":
    """
    Countries:
    SP = Spain           ---> P=10%
    UK = United Kingdom  ---> P=20%
    US = United States   ---> P=30%
    GE = Germany         ---> P=20%
    FR = France          ---> P=10%
    NL = The Netherlands ---> P=9%
    NULL                 ---> P=1%

    Status:
    PENDING              ---> P=20%
    COMPLETED            ---> P=50%
    FAIL                 ---> P=30%

    Amount:
    We generate a random sample of size 2000 from a Normal distribution with: 
        MEAN = 1e6 
        STANDARD DEVIATION = 1e5
    """
    country = np.random.choice(a=['SP', 'UK', 'US', 'GE', 'FR', 'NL', np.nan],
                               size= 2000,
                               p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.09, 0.01])
    
    status = np.random.choice(a=['PENDING', 'COMPLETED', 'FAILED'],
                              size=2000,
                              p=[0.2, 0.5, 0.3])
    
    amount = np.random.normal(loc=1e6, scale=1e5, size=2000)
    # We randomly set some null values in the amount
    mask = np.random.choice(a=[0,1], size=2000, p=[0.05, 0.95])
    amount[mask == 0] = np.nan
    # We simulate the creation of a dataframe from data coming in JSON format 
    # with fields 'id', 'country', 'status', 'amount'.
    # The id is automatically created by the index of the dataframe
    df_test = pd.DataFrame({'country':country, 'status':status, 'amount':amount})
    df_test.replace('nan', np.nan, inplace=True)
    transformer = DatasetConsumption(df_test)
    new_df = transformer.get_transformed_dataset()
    #Checks
    # Average outstanding = P(country)*P(pending)
    # Average outstanding France FR = P(FR) * P(pending) = 0.1 * 0.2 = 0.02
    # Average outstanding Spain SP = P(SP) * P(pending) = 0.1 * 0.2 = 0.02
    # Average outstanding United Kingdom = P(UK) * P(pending) = 0.2 * 0.2 = 0.04
    # Average outstanding United States = P(US) * P(pending) = 0.3 * 0.2 = 0.06
    # Average outstanding Germany = P(GE) * P(pending) = 0.2 * 0.02 = 0.04
    # Average outstanding The Netherlands = P(NL) * P(pending) = 0.09 * 0.2 = 0.018
    # Assume numeric error of 0.005
    epsilon = 0.005
    assert abs(new_df[new_df['country'] == 'FR']['average_outstanding'] - 0.02) <= epsilon
    assert abs(new_df[new_df['country'] == 'SP']['average_outstanding'] - 0.02) <= epsilon
    assert abs(new_df[new_df['country'] == 'UK']['average_outstanding'] - 0.04) <= epsilon
    assert abs(new_df[new_df['country'] == 'US']['average_outstanding'] - 0.06) <= epsilon
    assert abs(new_df[new_df['country'] == 'GE']['average_outstanding'] - 0.04) <= epsilon
    assert abs(new_df[new_df['country'] == 'NL']['average_outstanding'] - 0.018) <= epsilon

    # Amounts has been generated from a normal distribution centered at 1M. 
    # This distribution is symmetric, therefore 0.5 probability of getting an amount > 1M
    # and 0.5 probability of getting an amount < 0.5.
    # Critical rate = P(country) * P(amount > 1M) * P(failed)
    # Error rate = P(country) * P(amount <= 1M) * P(failed)
    


    