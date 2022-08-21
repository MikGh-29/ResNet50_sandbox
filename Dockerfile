FROM python:3.8-slim

WORKDIR /usr/src/app

ENV LISTEN_PORT=5000
EXPOSE 5000

RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    python3-dev \ 
    libjpeg-dev \
    zlib1g-dev \
    make \
    wget \
    libatlas-base-dev \
    libffi-dev 

RUN pip install torch==1.12.1 --user
RUN pip install torchvision==0.13.1 --user
RUN pip install flask==2.0.3 --user
RUN pip install Pillow==9.2.0 --user
RUN pip install validators==0.18.2 --user
RUN pip install requests==2.28.1 --user

COPY main.py .
COPY templates/ .
COPY templates/* templates/

CMD ["python", "main.py", "--host=0.0.0.0"]
