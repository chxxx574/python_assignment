import sqlite3
from datetime import datetime
import json
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

path = str(BASE_DIR / 'financial_data.db')

print(f"database path: {path}")

class Statistics:
    def __init__(self, start_date, end_date, symbol):
        self.financial_table = 'FINANCIAL'
        self.statistc_table = 'STATISTICS'
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol
        self.error_info = 0


    def main(self):
        cursor, conn = self.connect_database()
        query_result = self.query(cursor, conn)[0]
        result_data_list, result_info_list = [], []
        result = {}
        result_data, result_info = {}, {}
        result_data['symbol'] = self.symbol
        result_data['start_date'] = self.start_date
        result_data['end_date'] = self.end_date
        result_data['average_daily_open_price'] = query_result['average_daily_open_price']
        result_data['average_daily_close_price'] = query_result['average_daily_close_price']
        result_data['average_daily_volume'] =  query_result['average_daily_volume']
        result_info['error'] = self.get_error_info()
        result_data_list.append(result_data)
        result_info_list.append(result_info)
        result['data'] = result_data_list
        result['info'] =  result_info

        self.close_database(conn)
        return result

    def connect_database(self):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # print all tables
        sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
        # executing our sql query
        cursor.execute(sql_query)
        print("List of tables\n")
        # printing all tables list
        print(cursor.fetchall())

        return cursor, conn

    def query(self, cursor, conn):
        query_start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        query_end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        cursor.execute("SELECT * FROM " + self.financial_table + " WHERE date BETWEEN ? AND ? AND symbol = ?", (self.start_date, self.end_date, self.symbol))
        financial_data_from_databse = cursor.fetchall()

        if not financial_data_from_databse:
            self.error_info = 1
            result = [{'average_daily_open_price': '', \
                       'average_daily_close_price': '',
                       'average_daily_volume': ''}]
            return result
        # Since there is missing data in the database, here the interval is reduced to between the two dates that exist
        # and put into the database to avoid duplicate lookups
        existing_end_date = datetime.strptime(financial_data_from_databse[0][1], '%Y-%m-%d').date()
        existing_start_date = datetime.strptime(financial_data_from_databse[-1][1], '%Y-%m-%d').date()
        if existing_end_date <= query_end_date or existing_start_date >= query_start_date:
            query_end_date = max(query_start_date, existing_end_date)
            query_start_date = min(query_end_date, existing_start_date)
        cursor.execute("SELECT result FROM " + self.statistc_table + " WHERE date=? AND symbol=?",
                       (str(query_start_date) + '-' + str(query_end_date), self.symbol))
        statistic_data_from_database = cursor.fetchone()
        if statistic_data_from_database is not None:
            # If it already exists, the result is returned directly
            return json.loads(statistic_data_from_database[0])
        else:
            # Otherwise, query the data and store it in the statistic table
            data_to_cal = []
            cursor.execute("SELECT * FROM " + self.financial_table + " WHERE date BETWEEN ? AND ? AND symbol = ?", (query_start_date,  query_end_date, self.symbol))
            statistic_data_from_database = cursor.fetchall()
            for data in statistic_data_from_database:
                data_to_cal.append(data)
            cal_statistic_result = self.cal_statistic_result(data_to_cal)
            result = [{'date': str(query_start_date) + '-' + str(query_end_date), 'average_daily_open_price': cal_statistic_result[0],\
                 'average_daily_close_price': cal_statistic_result[1], 'average_daily_volume': cal_statistic_result[2]}]
            result_str = json.dumps(result)
            cursor.execute(
                "INSERT INTO " + self.statistc_table + " (symbol, date, result) VALUES (?, ?, ?)",
                (self.symbol, str(query_start_date) + '-' + str(query_end_date), result_str))
            conn.commit()
            return result

    def cal_statistic_result(self, data_to_cal):
        average_daily_open_price_list = []
        average_daily_close_price_list = []
        average_daily_volume_list = []
        result = []
        # data:(symbol, date, open_price, close_price, volume)
        for data in data_to_cal:
            average_daily_open_price_list.append(float(data[2]))
            average_daily_close_price_list.append(float(data[3]))
            average_daily_volume_list.append(float(data[4]))

        average_daily_open_price = sum(average_daily_open_price_list) / len(average_daily_open_price_list)
        average_daily_close_price_list = sum(average_daily_close_price_list) / len(average_daily_close_price_list)
        average_daily_volume_list = sum(average_daily_volume_list) / len(average_daily_volume_list)

        result.append("{:.2f}".format(average_daily_open_price))
        result.append("{:.2f}".format(average_daily_close_price_list))
        result.append("{:.2f}".format(average_daily_volume_list))

        return result

    def close_database(self, conn):
        conn.close()

    def get_error_info(self):
        if self.error_info == 0:
            info = ''
        if self.error_info == 1:
            info = "We do not have data for this period"

        return info


if __name__ == '__main__':
    a = Statistics('2023-01-01',  '2023-01-31', 'IBM')
    a.main()

