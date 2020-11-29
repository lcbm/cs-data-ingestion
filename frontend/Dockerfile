FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./frontend/requirements.txt ./
RUN pip install -r requirements.txt

COPY ./frontend ./frontend/
COPY ./frontend/wsgi.py ./
COPY ./env.d/frontend.env ./

ENV FLASK_ENV=production
CMD ["gunicorn", "--workers=2", "wsgi:app", "--timeout 1000", "--bind", "0.0.0.0:5000"]
