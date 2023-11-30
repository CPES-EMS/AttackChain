from AttackChain import AttackChain
from DataLoader import DataLoader
from config import *
import traceback
import logging
import os
from datetime import datetime
import json
from OutPutHandler import OutPutHandler


def init_logging():
    LOG_PATH = os.path.join(os.getcwd(), LOG_FILE_DIR)
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    LOG_FILE_NAME = os.path.join(LOG_PATH, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("logging init success")
    return True
    

def main():
    init_logging()
    dataLoader = DataLoader()
    outputHandler = OutPutHandler()
    start_time = '2021-09-08 15:00:00'
    end_time = '2021-09-08 19:00:00'
    table_name = '202109'
    if IS_CONNECT_DB:
        try:
            alert_data = dataLoader.load_from_sql(start_time=start_time, end_time=end_time, table_name=table_name)
            logging.info("reading data from sql OK")
        except Exception as e:
            print(f"ERROR, {e}")
            logging.debug(traceback.format_exc())
            print(f"cannot fetch data from database!")
            return -1
    else:
        try:
            alert_data = dataLoader.load_from_csv(csv_file='input.csv')
            logging.info("reading data from csv file OK")
        except Exception as e:
            print(f"ERROR, {e}")
            logging.debug(traceback.format_exc())
            print(f"Please check input file again!")
            return -1
    attackChain = AttackChain(alert_data)
    chainResult = attackChain.getAttackChain()
    if IS_CONNECT_DB:
        try:
            outputHandler.output_write_database(chainResult, end_time)
            logging.info("writing data to database OK")
        except Exception as e:
            print(f"ERROR, {e}")
            logging.debug(traceback.format_exc())
            print(f"cannot write into database!")
            return -1
    else:
        try:
            outputHandler.output_json(chainResult)
            logging.info("writing data to json OK")
        except Exception as e:
            print(f"ERROR, {e}")
            logging.debug(traceback.format_exc())
            print(f"Please check output file again!")
            return -1


if __name__ == '__main__':
    main()
    