FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . /app
VOLUME /app
 
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf .github .git dockerfile requirements.txt
#USER 99[:100]
LABEL org.opencontainers.image.source https://github.com/NathanWarrick/Office-National-Scraper

CMD [ "python", "-u", "main.py" ]
