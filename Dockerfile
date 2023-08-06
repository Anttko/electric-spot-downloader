FROM python:3.9.5-slim-buster
WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 
RUN python -m pip install --upgrade pip

COPY . . 
RUN pip install -r requirements.txt

ADD crontab /etc/cron/crontab
RUN chmod 0644 /etc/cron/crontab
RUN touch /var/log/cron.log
RUN chmod 0744 electric_price_downloader/electric_data_downloader.py
RUN chmod 0744 electric_price_downloader/csv_reader.py
RUN chmod 0744 electric_price_downloader/send_to_server.py


RUN apt-get install -y cron

CMD ["cron", "-f"]
