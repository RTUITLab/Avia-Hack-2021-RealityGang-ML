FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./ /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]