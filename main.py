
from argparse import ArgumentParser
from src.challenge import DatasetConsumption
import time

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
    main()