FROM python:3-alpine3.7
# FROM frolvlad/alpine-miniconda3

COPY . /app
WORKDIR /app

ENV GOOGLE_APPLICATION_CREDENTIALS /app/twitter-bots-239422-6d378e648ea2.json

# RUN apk add make automake gcc g++ subversion python3-dev
# RUN conda install numpy
# RUN conda install scipy
RUN pip3 install -r requirements.txt

ENTRYPOINT python3 followers/prob_bot.py