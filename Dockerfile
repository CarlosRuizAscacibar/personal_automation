FROM ubuntu:18.04
MAINTAINER Carlos Ruiz

# Install cron
RUN apt-get update && apt-get install -y cron
RUN sudo apt-get install firefox-esr

#installs geckodriver
INSTALL_DIR="/usr/local/bin"

url="https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"
curl -s -L "$url" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$INSTALL_DIR"
echo "installed geckodriver binary in $INSTALL_DIR"

#configure virtual env
pip install virtualenv
python -m virtualenv env --python=/usr/bin/python3.7
pip install -r requeriments.txt


#add cronjobs
crontab example_crontab.txt