FROM python:2.7
WORKDIR /workspace
COPY . /workspace

# Environment Variables for future use
ENV BOT_TOKEN
ENV UPDATE_INTERVAL=300

RUN mkdir /workspace/resources/userdata
RUN pip install -r requirements.txt
CMD python rssbot.py
