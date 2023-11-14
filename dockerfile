FROM python:3.10.13-alpine3.17

WORKDIR /app

COPY . /app

RUN pip3 install -r linux-requirements.txt

EXPOSE 8000

#Initiate the uvicorn server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]