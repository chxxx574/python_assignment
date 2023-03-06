# A brief project description
Task1: get data from API (2 weeks) and put the data into database

Local boot:
·Mac & Linux: 
```
API_KEY=0TSJEOCNJMAYP9JE python ./get_raw_data.py
```
·Windows: 
```
set API_KEY=0TSJEOCNJMAYP9JE && python ./get_raw_data.py
```

Task2: Access the database and respond to relevant statistics

to get the information:
```
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-03-01&end_date=2023-03-04&symbol=IBM&limit=3&page=2'
```

to get the statistcs:
```
curl -X GET http://localhost:5000/api/statistics?start_date=2023-03-01&end_date=2023-03-04&symbol=IBM

```

# Tech stack you are using in this project：

 Use fastapi /uvicorn  as webserver
 Use sqlite as databse


# How to run your code in local environment

1. use get_raw_data.py to get data from API, you can change the self.Duration to get different duration from today. Then we creat the database financial_data.db, we write the data into financial_data and put into database. If the database has existed, we will print 'Database financial_data already exists'.

2. use get_financial_data to get the data from database with the time period and symbol.

3. use get_statistics to get the statistic data from database with the time period and symbol.
we add a new table to store the data, if this data will be request for many times, this method will 
save lots of time. Because there is missing data, we store the data for the maximum existence time interval.

# Provide a description of how to maintain the API key to retrieve financial data from AlphaVantage in both local development and production environment.

To retrieve financial data from AlphaVantage API, an API key is required. The API key is a secret value that should be kept confidential and securely stored. 
Use environment variables: Store the API key as an environment variable rather than hard-coding it in your code. This way, you can keep the key confidential and change it easily if needed.


 # error handling
 We added the code related to error handling, but due to time constraints, only the following cases are supported for the time being, and the code can be easily modified and cases added subsequently.
 1. we can handle some error, but due to the time is limited for this task, this part can be improved both in containing more situation and better code structure.
 2. If there is no data in the query interval, we will return We do not have data for this period
 3. If there is no start_data, we will return 'Please input start_date'.
 4. We set a number of defaults, such as symbol='IBM'

 

