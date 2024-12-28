FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "app.py"]