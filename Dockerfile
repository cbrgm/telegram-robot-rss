FROM python:2.7
WORKDIR /workspace
COPY . /workspace

# Environment Variables for future use
ENV BOT_TOKEN telegram_bot_token
ENV UPDATE_INTERVAL 300

RUN mkdir /workspace/resources/userdata
RUN pip install -r requirements.txt
CMD python .docker/initconfig.py && python robotrss.py
