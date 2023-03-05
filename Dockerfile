FROM python:3.6

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/

ENV PORT 5000

EXPOSE $PORT

# 启动应用程序
CMD ["python", "/app/financial/main.py"]


# docker build -t assigenment-app .

# docker run -e API_KEY=0TSJEOCNJMAYP9JE --rm -p 5000:5000 assigenment-app
# docker run -e API_KEY=0TSJEOCNJMAYP9JE -it --rm -p 5000:5000 assigenment-app /bin/bash
