import csv
import mysql.connector
from datetime import datetime


class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.database = database
        self.cursor = self.conn.cursor()
        self._create_database()

    # 기초 DB 생성
    def _create_database(self):
        self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
        self.cursor.execute(f'USE {self.database}')

    # 테이블 생성
    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS mars_weather (
            weather_id INT AUTO_INCREMENT PRIMARY KEY,
            mars_date DATETIME NOT NULL,
            temp INT,
            storm INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    # DB 튜플 입력
    def insert_data(self, mars_date, temp, storm):
        query = '''
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
        '''
        self.cursor.execute(query, (mars_date, int(temp), storm)) # 여기서 temp를 int로 변환
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

# csv 파일 로드해서 DB에 넣기
def load_csv_and_insert(filename, db_helper):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.strptime(row['mars_date'], '%Y-%m-%d')
            temp = float(row['temp']) # CSV에 실수로 들어가 있어 일단 float로 변환
            storm = int(row['stom'])  # CSV에는 stom으로 되어 있음
            db_helper.insert_data(date, temp, storm)


if __name__ == '__main__':
    db = MySQLHelper(
        host='localhost',
        user='root',
        password='1234', # ← 사용자 비밀번호 입력
        database='codyssey'
    )
    db.create_table()
    load_csv_and_insert('mars_weathers_data.CSV', db)
    db.close()