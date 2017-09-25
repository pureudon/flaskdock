FROM python:3.6.1
MAINTAINER pureudon <pureudonhk@gmail.com>

# init user and working directory
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask
RUN mkdir -p /home/flask/app/web
WORKDIR /home/flask/app/web

# install python packages with requirements.txt
COPY requirements.txt /home/flask/app/web
RUN pip install --no-cache-dir -r requirements.txt

# copy src code to working directory
COPY . /home/flask/app/web
RUN chown -R flask:flaskgroup /home/flask

# login user as
USER flask
