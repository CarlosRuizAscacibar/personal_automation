# /bin/bash

#is firefox installed
firefox --version  > /dev/null 2&> /dev/null;
is_installed=$?

if ["$is_installed" -eq "0"]; then
    sudo apt-get install firefox-esr
    echo "installed firefox esr"
fi


#installs geckodriver
INSTALL_DIR="/usr/local/bin"

url="https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz"
curl -s -L "$url" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$INSTALL_DIR"
echo "installed geckodriver binary in $INSTALL_DIR"

git clone https://github.com/CarlosRuizAscacibar/personal_automation.git

cd personal_automation
pip install virtualenv
python -m virtualenv env --python=/usr/bin/python3.7
source env/bin/activate
sudo apt-get install libatlas-base-dev
pip install -r requeriments.txt
python -c "from shutil import which; print(which('firefox') != None)"


#
crontab example_crontab.txt