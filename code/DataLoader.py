import pymysql
from config import *
import pandas as pd

class DataLoader:
    def __init__(self) -> None:
        self.DB_SERVER = DB_SERVER
        self.DB_PORT = DB_PORT
        self.DB_USERNAME = DB_USERNAME
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_NAME = DB_NAME

    def getconn(self):
        conn = pymysql.connect(host=self.DB_SERVER, port=self.DB_PORT, user=self.DB_USERNAME, passwd=self.DB_PASSWORD, db=self.DB_NAME, charset='utf8mb4')
        return conn

    def load_from_csv(self, csv_file='input.csv'):
        data = pd.read_csv(csv_file)
        data = data[["sip", "dip", "receivetime", "sport", "dport", "category", "severity", "id"]]
        return [tuple(alert) for alert in data.values]
    

    def load_from_sql(self, start_time, end_time, table_name):
        conn = self.getconn()
        cursor = conn.cursor()
        sql = "SELECT sip, dip, receivetime, sport, dport, category, severity, id FROM `" + table_name + "` WHERE receivetime>=%s" \
                + " and receivetime<=%s"
        sqlArgs = [start_time, end_time]
        cursor.execute(sql, sqlArgs)
        data = cursor.fetchall()
        conn.close()
        cursor.close()
        return data