import uvicorn
from fastapi import FastAPI
from get_finacial_data import Query
from get_statistics import Statistics
app = FastAPI()


@app.get("/api/financial_data")
def main(start_date, end_date, symbol, limit, page):
    query = Query(start_date, end_date, symbol, limit, page)
    result = query.main()
    return result


@app.get("/api/statistics")
def statistics(start_date, end_date, symbol):
    statistics = Statistics(start_date, end_date, symbol)
    result = statistics.main()
    return result


if __name__ == "__main__":
    uvicorn.run(app, port=5000, host="0.0.0.0", log_level="info")
