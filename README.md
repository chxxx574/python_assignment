README.md:

You should include:

A brief project description

Tech stack you are using in this project
fastapi /uvi 作为webserver
交代一下数据库

How to run your code in local environment
程序运行逻辑

Provide a description of how to maintain the API key to retrieve financial data from AlphaVantage in both local development and production environment.

> To retrieve financial data from AlphaVantage API, an API key is required. The API key is a secret value that should be kept confidential and securely stored. Here are some best practices for maintaining the API key in both local development and production environments:

Use environment variables: Store the API key as an environment variable rather than hard-coding it in your code. This way, you can keep the key confidential and change it easily if needed.
