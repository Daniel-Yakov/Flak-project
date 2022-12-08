FROM python:alpine3.17

WORKDIR /app
COPY . .
RUN pip install -r requirments.txt
ENTRYPOINT ["python3", "chat.py"]