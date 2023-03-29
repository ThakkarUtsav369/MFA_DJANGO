FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir /static
RUN pip install --upgrade pip
#RUN apt-get -y update && apt-get -y install nginx


ADD requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
ADD . ./
RUN chmod +x ./docker-entrypoint.sh
# RUN sed -i 's/\r$//g' ./beat-entrypoint.sh
# RUN chmod +x ./beat-entrypoint.sh

# RUN chmod +x ./docker-entrypoint-local.sh
# RUN chmod +x ./beat-entrypoint.sh
# ADD ./static/logo-color.png ./code/static
#FROM nginx:1.16.0-alpine
#RUN rm /etc/nginx/conf.d/default.conf
#COPY ./nginx.conf /etc/nginx/conf.d

# CMD gunicorn raychemrpg.wsgi:application --bind 0.0.0.0:$PORT