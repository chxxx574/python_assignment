import sqlite3
from datetime import datetime
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

path = str(BASE_DIR / 'financial_data.db')

class Query:
    def __init__(self, start_date, end_date, symbol, limit=3, page=2):
        self.financial_table = 'FINANCIAL'
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol
        self.limit = limit
        self.page = page

    def main(self):
        cursor, conn = self.connect_database()
        result_list = self.search_data(cursor)
        self.close_database(conn)
        return result_list

    def connect_database(self):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        return cursor, conn

    def search_data(self, cursor):
        if self.start_date == self.end_date:
            cursor.execute("SELECT * FROM " + self.financial_table + " WHERE date = ?", (self.start_date))
        else:
            cursor.execute("SELECT * FROM " + self.financial_table + " WHERE date BETWEEN ? AND ? AND symbol = ?", (self.start_date, self.end_date, self.symbol))
        rows = cursor.fetchall()
        result_list = []
        result = {}
        # row = ('symbol', 'date', 'open_price', 'close_price', 'volume')
        for row in rows:
            result_dict = {}
            result_dict['symbol'] = row[0]
            result_dict['date'] = row[1]
            result_dict['open_price'] = row[2]
            result_dict['close_price'] = row[3]
            result_dict['volume'] = row[4]
            result_list.append(result_dict)
        result['data'] = result_list
        return result


    def close_database(self, conn):
        conn.close()

if __name__ == '__main__':
    a = Query('2023-03-01',  '2023-03-03', 'IBM')
    result = a.main()
    print(result)