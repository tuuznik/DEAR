FROM python:3.8-slim

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./ /DEAR/

CMD ["gunicorn", "-w", "2", "-b", ":8081", "DEAR.app:app"]