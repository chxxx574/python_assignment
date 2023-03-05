import json
import requests
import datetime
import sqlite3
import os

API_KEY = os.getenv("API_KEY", None)

# 本地启动
# Mac & Linux: API_KEY=0TSJEOCNJMAYP9JE python ./get_raw_data.py
# Windows: set API_KEY=0TSJEOCNJMAYP9JE && python ./get_raw_data.py

if API_KEY is None:
    raise Exception("You should provide a environment variable API_KEY")


class DataProcess:
    def __init__(self, file_name='financial_data', database='financial_data'):
        # two weeks
        self.Duration = 14
        self.file_name = file_name
        self.database = database

    def get_data_from_API(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey={API_KEY}'
        r = requests.get(url)
        data = r.json()
        return data

    def process_data2Json(self, data):
        testarr = []
        Default_days = []
        date_today = datetime.date.today()
        # API only provides data up to one day old
        date_begin = date_today - datetime.timedelta(days=1)
        for day in range(self.Duration):

            date = date_begin - datetime.timedelta(days=day)

            if str(date) not in data['Time Series (Daily)']:
                Default_days.append(date)
                continue
            dict_day = {}
            dict_day['symbol'] = data['Meta Data']['2. Symbol']
            dict_day['date'] = date.strftime('%Y-%m-%d')
            dict_day['open_price'] = data['Time Series (Daily)'][str(
                date)]['1. open']
            dict_day['close_price'] = data['Time Series (Daily)'][str(
                date)]['4. close']
            dict_day['volume'] = data['Time Series (Daily)'][str(
                date)]['6. volume']
            testarr.append(dict_day)
        return testarr, Default_days

    def write_to_file(self, testarr):
        file = open(self.file_name, 'w')
        for data in testarr:
            json.dump(data, file, indent=10)
            file.write(',' + '\n')

    def add_to_database(self, testarr):
        conn = sqlite3.connect(self.database + '.db')
        c = conn.cursor()
        for dict_day in testarr:
            sql = "INSERT INTO FINANCIAL (symbol, date, open_price, close_price, volume)\
                   VALUES ('{}', '{}', {}, {}, {});".format(dict_day['symbol'], dict_day['date'], dict_day['open_price'], dict_day['close_price'], dict_day['volume'])
            c.execute(sql)
            conn.commit()
        conn.close()

    def creat_database(self):
        try:
            conn = sqlite3.connect(self.database+'.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE FINANCIAL 
                        (symbol TEXT,
                           date DATE,
                           open_price TEXT,
                           close_price TEXT,
                           volume TEXT);''')
            c.execute('''CREATE TABLE STATISTICS 
                                    (symbol TEXT,
                                       date DATE,
                                       result TEXT);''')

            conn.commit()
            conn.close()
        except:
            print('table financial_data already exists')


if __name__ == '__main__':
    D = DataProcess()
    data = D.get_data_from_API()
    jtext, Default_days = D.process_data2Json(data)
    D.creat_database()
    D.add_to_database(jtext)
    print(1)
