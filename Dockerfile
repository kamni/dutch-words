FROM python:3.12.8-bookworm

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
COPY ./requirements_dev.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

COPY run_server.py .
COPY . .
