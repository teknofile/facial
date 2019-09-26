FROM python:alpine


RUN apk update && apk add \
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
  pngquant \
  sqlite \
  sqlite-dev

ADD ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY src /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/main.py"]
