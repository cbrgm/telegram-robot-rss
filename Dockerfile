FROM python:2.7
WORKDIR /workspace
COPY . /workspace

RUN mkdir /workspace/resources/userdata
RUN pip install -r requirements.txt
CMD python rssbot.py
