FROM python:3.9-slim
# Basic Packages install
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    gnupg \
    lsb-release \
    git \
    apt-utils \
    python3-dev \
    python3-distutils \
    python3-pip \
    unzip \
    sudo \
    wget \
    software-properties-common \
    vim \
    figlet \
    toilet \
    mc \
    featherpad \
    dos2unix \
    tmux \
    libpoco-dev \
    libeigen3-dev
WORKDIR /app


COPY sample.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["/bin/bash", "-c" ]