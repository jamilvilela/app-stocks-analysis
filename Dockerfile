FROM python:3.10

RUN apt install python3.10-venv
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

EXPOSE 5000

CMD ["python", "src/app.py", "--host", "0.0.0.0", "--port", "5000"]
