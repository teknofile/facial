FROM python:alpine

RUN apk update && apk add \
  build-base \
  cmake \
  libjpeg \
  zlib-dev \
  tiff-dev \
  freetype freetype-dev \
  lcms lcms-dev \
  lcms2 lcms2-dev lcms2-utils \
  libwebp libwebp-tools libwebp-dev \
  openjpeg openjpeg-tools openjpeg-dev \
  pngquant \
  sqlite sqlite-dev \
  openblas openblas-dev

RUN adduser -D facial

WORKDIR /home/facial

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY facial.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP facial.py

RUN chown facial:facial ./

USER facial

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
