FROM python:alpine


RUN apk update 
RUN apk add \
  build-base \
  cmake \
  libjpeg \
  zlib-dev \
  tiff-dev \
  freetype \
  freetype-dev \
  lcms \
  lcms-dev \
  lcms2 \
  lcms2-dev \
  lcms2-utils \
  libwebp \
  libwebp-tools \
  libwebp-dev \
  openjpeg \
  openjpeg-tools \
  openjpeg-dev \
  pngquant 

#RUN pip3 install \
#  flask \
#  utils \
#  dlib \
#  face_recognition \
#  imutils \

RUN pip3 install -r requirements.txt

COPY src /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/app.py"]
