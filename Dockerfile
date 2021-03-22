#FROM python:3.8.5
#WORKDIR /code
#COPY . .
#RUN pip install -r requirements.txt
#CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
##CMD gunicorn --bind 0.0.0.0:8000 foodgram.wsgi

FROM python:3.8.5
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install -r ./requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
