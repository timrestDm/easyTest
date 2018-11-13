FROM python:3.6
RUN mkdir -p /code/easyTest
WORKDIR /code
ADD ./requirements.txt /code
RUN pip3 install -r requirements.txt