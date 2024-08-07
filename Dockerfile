FROM python:3.10-alpine

WORKDIR /project

# Установка системных зависимостей
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    apk add --no-cache postgresql-libs

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /project

ENTRYPOINT ["python", "main.py"]