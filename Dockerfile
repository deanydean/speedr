#
# Speed Docker container image
#
FROM debian:10

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN mkdir /speedr && \
    useradd --system --home-dir /speedr speedr && \
    chown speedr /speedr

ADD app.py /speedr/app.py
ADD requirements.txt /speedr/requirements.txt

WORKDIR /speedr
USER speedr

RUN pip3 install -r requirements.txt

CMD [ ".local/bin/flask", "run", "--host=0.0.0.0", "--port=5000" ]