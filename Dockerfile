FROM tiangolo/uwsgi-nginx-flask
RUN apt update
RUN apt install nano
RUN pip uninstall JWT
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY ./app /app

CMD [ "python3", "server.py" ]
