FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "hammer_systems.wsgi.application", "--bind", "0.0.0.0:8000" ]