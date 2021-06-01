FROM python:3.8.1

WORKDIR /chall

COPY . /chall

RUN pip install -r "/chall/requirements.txt"

EXPOSE 5000

CMD ["python", "/chall/main.py"]