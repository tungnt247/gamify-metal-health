FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5555

ENV FLASK_APP=app/__init__.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5555"]
