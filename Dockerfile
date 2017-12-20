FROM python:3.6-alpine

RUN mkdir -p /sjghbot
ADD . /sjghbot/

RUN pip3 install --no-cache-dir --upgrade pip six
RUN pip3 install -r /sjghbot/requirements.txt

CMD ["python", "/sjghbot/sjghbot.py"]
