FROM python:3.10-slim

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/src


COPY requirements.txt /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY recipify /opt/app/recipify/

WORKDIR /opt/app/

RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache/
RUN pip install gunicorn

WORKDIR /opt/app/recipify/

EXPOSE 8080
STOPSIGNAL SIGTERM
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
