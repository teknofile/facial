FROM python:alpine


RUN apk update 
RUN apk add \
  build-base \
  cmake

RUN pip3 install \
  flask \
  utils \
  dlib \
  face_recognition \
  imutils

RUN pip3 install dlib face_recognition imutils

COPY src /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/app.py"]
