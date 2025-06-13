FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt && pip install setuptools

COPY . /app

EXPOSE 9000

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
