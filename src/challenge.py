import pandas as pd
import numpy as np
from argparse import ArgumentParser
import time

class DatasetConsumption:
    def __init__(self, dataset:pd.DataFrame):
        self.df = dataset

    def get_transformed_dataset(self)->pd.DataFrame:
        self.df(dropna=True)
        df_t = pd.DataFrame()
        
    



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
    print(np.where(np.isnan(amount)))
    print(df_test.head(10))
    N = len(df_test)
    df_test.dropna(inplace=True)
    df = pd.DataFrame()
    df = df_test.groupby('country', as_index=False, dropna=True)['status'].agg(lambda y: sum([1 if x == 'PENDING' else 0 for x in y])/N )
    df_test.groupby('country', as_index=False, dropna=True)['status', 'amount'].agg(lambda y: [1 if x[] == ])



    