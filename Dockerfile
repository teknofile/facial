FROM python:alpine

RUN pip3 install flask utils

RUN apk update && apk add build-base

RUN pip3 install dlib face_recognition imutils

COPY src /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/app.py"]
