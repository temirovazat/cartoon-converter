FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1\
    PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get -y install gcc

ADD . /app/

RUN pip install --default-timeout=1000 poetry \
  && poetry config virtualenvs.create false\
  && poetry export --without-hashes -f requirements.txt > requirements.txt\
  && sed -e "s/Skipping virtualenv creation, as specified in config file.//g" -i requirements.txt\
  && pip install --default-timeout=1000 -r requirements.txt

ENTRYPOINT ["python3", "/app/src/app.py"] 