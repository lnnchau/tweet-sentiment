FROM ubuntu:18.04

RUN apt-get update -qqy && \
  apt-get install -y \
  build-essential \
  cmake \
  curl \
  g++ \
  git \
  libsm6 \
  libxrender1 \
  locales \
  pkg-config \
  python3-dev \
  python3-pip \
  software-properties-common \
  wget \
  unzip

# Set default python version
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install -U pip setuptools

# Copy files
ADD . /opt/code
WORKDIR /opt/code

RUN pip install -r requirements.txt
RUN apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

VOLUME [ "/data", "/logs" ]
RUN chmod +x ./entrypoint.sh
CMD [ "./entrypoint.sh" ]