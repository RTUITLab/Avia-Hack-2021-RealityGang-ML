FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY ./ /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn main:app --host 127.0.0.1 --port 8000