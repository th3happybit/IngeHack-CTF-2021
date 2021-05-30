FROM python:3.6
COPY ./challenge /app
WORKDIR /app
RUN pip install flask flask_socketio flask_restful eventlet
EXPOSE 5000
ENTRYPOINT ["python", "/app/app.py"]