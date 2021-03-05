
from argparse import ArgumentParser
from src.challenge import DatasetConsumption
import time
import logging
import os

def manage_arguments():
    parser = ArgumentParser()
    parser.add_argument('--output-type',
                        help="Indicates whether the transformed dataset will be stored: 'csv', 's3' or 'postgres' ",
                        metavar='output')
    return parser.parse_args()

def main(args):
    output = args.output
    assert output == 'csv' or output == 's3' or output == 'postgres', "Output should be 'csv', 's3' or 'postgres'"
    curr_dir = os.getcwd()
    logging_file = os.path.join(curr_dir, 'logs', 'execution_times.log')

    logging.basicConfig(filename= logging_file, filemode='w', 
                        format='%(process)d-%(levelname)s-%(message)s',
                        datefmt = '%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

    consumer = DatasetConsumption()
    start_time = time.time()
    df_new = consumer.get_transformed_dataset()
    logging.info(f" --- time (seconds) -- {time.time() - start_time}")


    
if __name__ == "__main__":
    args = manage_arguments()
    main(args)