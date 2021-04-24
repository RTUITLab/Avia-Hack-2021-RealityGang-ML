FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]