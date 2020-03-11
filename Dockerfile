FROM ubuntu:18.04
MAINTAINER Amin Fadaee

USER root
WORKDIR /root

RUN apt-get update
RUN apt-get install -y python3 python3-pip wget curl
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP url_shortner.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY . .

CMD ["python3", "-m", "flask", "run"]