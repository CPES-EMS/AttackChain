import pymysql
import json
from config import *
import os


class OutPutHandler:
    def __init__(self) -> None:
        self.attackChainTableName = AttackChainTableName

    def output_json(self, chainResult):
        json_str = json.dumps(chainResult, ensure_ascii=False, indent=4)
        OUTPUT_FILE_PATH = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8')as f:
            f.write(json_str)
        f.close()

    def getconn(self):
        conn = pymysql.connect(host=self.DB_SERVER, port=self.DB_PORT, user=self.DB_USERNAME, passwd=self.DB_PASSWORD, db=self.DB_NAME, charset='utf8mb4')
        return conn
    
    def sqlstr(self, a):
        return '"' + str(a) + '"'

    def create_chain_table(self):
        conn = self.getconn()
        cursor = conn.cursor()
        sql='CREATE TABLE IF NOT EXISTS ' + self.attackChainTableName +\
            '(id INT NOT NULL AUTO_INCREMENT,'\
            'gen_time TEXT,'\
            'number INT,'\
            'spanNumber INT,'\
            'first_chain TEXT,' \
            'second_chain TEXT,'\
            'third_chain TEXT,'\
            'others TEXT,'\
            'PRIMARY KEY (id))'
        cursor.execute(sql)
        conn.close()
        cursor.close()


    def output_write_database(self, chainResult, end_time):
        self.create_chain_table()
        conn = self.getconn()
        cursor = conn.cursor()
        gen_time = self.sqlstr(end_time)
        for attackchain in chainResult:
            number = int(attackchain['number'])
            spanNumber = int(attackchain['spanNumber'])
            first_chain = self.sqlstr(attackchain['first_chain'])
            second_chain = self.sqlstr(attackchain['second_chain'])
            third_chain = self.sqlstr(attackchain['third_chain'])
            others = self.sqlstr(attackchain['others'])
            sql = "INSERT INTO `" + self.attackChainTableName + "`" +  "(gen_time,number,spanNumber,first_chain,second_chain,third_chain,others)"\
                + "VALUES (%s,%d,%d,%s,%s,%s,%s);"\
                %(gen_time,number,spanNumber,first_chain,second_chain,third_chain,others)
            print(sql)
            cursor.execute(sql)
            conn.commit()
        conn.close()
        cursor.close()

