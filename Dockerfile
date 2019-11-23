FROM ubuntu:18.04
MAINTAINER Carlos Ruiz

# Install cron
RUN apt-get update && apt-get install -y cron
RUN sudo apt-get install firefox-esr

#installs geckodriver
RUN INSTALL_DIR="/usr/local/bin"

RUN url="https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"
RUN curl -s -L "$url" | tar -xz
RUN chmod +x geckodriver
RUN sudo mv geckodriver "$INSTALL_DIR"
RUN echo "installed geckodriver binary in $INSTALL_DIR"

#configure virtual env
RUN pip install virtualenv
RUN python -m virtualenv env --python=/usr/bin/python3.7
RUN pip install -r requeriments.txt


#add cronjobs
RUN crontab example_crontab.txt