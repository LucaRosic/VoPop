FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .

# Packages to install for selenium
RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y ca-certificates curl

#### FIREFOX
ARG firefox_ver=129.0.2
ARG geckodriver_ver=0.35.0
ARG build_rev=0


RUN apt-get update \
   && apt-get upgrade -y \
   && apt-get install -y --no-install-recommends --no-install-suggests \
   ca-certificates \
   && update-ca-certificates \
   \
   # Install tools for building
   && toolDeps=" \
   curl bzip2 \
   " \
   && apt-get install -y --no-install-recommends --no-install-suggests \
   $toolDeps \
   \
   # Install dependencies for Firefox
   && apt-get install -y --no-install-recommends --no-install-suggests \
   libgl1 libpci3 \
   `apt-cache depends firefox-esr | awk '/Depends:/{print$2}'` \
   \
   # Download and install Firefox
   && curl -fL -o /tmp/firefox.tar.bz2 \
   https://ftp.mozilla.org/pub/firefox/releases/${firefox_ver}/linux-x86_64/en-GB/firefox-${firefox_ver}.tar.bz2 \
   && tar -xjf /tmp/firefox.tar.bz2 -C /tmp/ \
   && mv /tmp/firefox /opt/firefox \
   \
   # Download and install geckodriver
   && curl -fL -o /tmp/geckodriver.tar.gz \
   https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz \
   && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
   && chmod +x /tmp/geckodriver \
   && mv /tmp/geckodriver /usr/local/bin/ \
   \
   # Cleanup unnecessary stuff
   && apt-get purge -y --auto-remove \
   -o APT::AutoRemove::RecommendsImportant=false \
   $toolDeps \
   && rm -rf /var/lib/apt/lists/* \
   /tmp/*

ENV MOZ_HEADLESS=1

RUN pip install --upgrade pip

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

# NLTK punkt package
RUN python -m nltk.downloader punkt_tab

COPY . .

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]