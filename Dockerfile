FROM python:3.8-slim

RUN apt update && apt install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./ /DEAR/

ENV PYTHONPATH "${PYTHONPATH}:/DEAR/"

CMD ["gunicorn", "-w", "2", "-b", ":8080", "DEAR.app:app"]