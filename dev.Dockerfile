FROM python:3.9.5-slim-buster
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/sbin:$PATH"

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 
RUN python -m pip install --upgrade pip

COPY . . 
RUN pip install -r requirements.txt
RUN apt-get install -y cron
ADD crontab /etc/cron/crontab
RUN crontab /etc/cron/crontab
CMD [ "crond" , "-d"]




#CMD ["python3", "electric_data_downloader.py"]


FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY . . 
RUN pip install -r ./requirements.txt
RUN apt-get install -y cron

RUN crontab crontab

CMD [ "crond" , "-d"]



