FROM python:3.8-alpine

RUN pip install fastapi uvicorn aiofiles
RUN adduser -D ingehack
COPY ./app /home/ingehack/app

RUN chown ingehack:root /home/ingehack/app -R

USER ingehack
WORKDIR /home/ingehack/app
EXPOSE 5000
CMD ["python", "main.py"]