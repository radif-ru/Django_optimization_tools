FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/www/geekshop
WORKDIR /var/www/geekshop
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/var/www/geekshop/entrypoint.sh"]
