FROM python:3.12.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "fastapi", "run", "main.py" ]

CMD ["--host", "0.0.0.0", "--port", "8000"]