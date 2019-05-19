FROM python:3.7-alpine

RUN apk add gcc musl-dev libffi-dev

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD bot.py /

CMD [ "python", "./bot.py" ]
