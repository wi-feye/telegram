FROM python:3.8
#FROM conda/miniconda3:latest
LABEL maintainer="Wi-Feye"
LABEL version="1.0"
LABEL description="Wi-Feye Telegram Bot"

# copying the environment
COPY . /app

# setting the workdir
WORKDIR /app

# installing all requirements
RUN ["pip3", "install", "-r", "requirements.txt"]

# exposing the port
EXPOSE 10006/tcp

# main command
CMD python3 main.py
