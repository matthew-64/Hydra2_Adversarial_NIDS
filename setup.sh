#!/usr/bin/env bash

# prerequisites
apt-get update
apt-get install -y \
  curl \
  gnupg \
  apt-transport-https \
  lsb-release \
  mininet \
  nmap \
  hping3 \
  python-django \
  python-pandas \
  python-pip \
  libpcap-dev \
  flex \
  bison

# pip installs
pip3 install -r "requirements.txt"

# Argus - server
for version in "argus-3.0.8.1" "argus-clients-3.0.8"
do
  wget "http://qosient.com/argus/src/${version}.tar.gz"
  tar -xvzf "${version}.tar.gz"
  ( \
    cd ${version}; \
    ./configure; \
    make; \
    make install; \
  )
  rm -rf ${version}*
done

# faucet
echo "deb https://packagecloud.io/faucetsdn/faucet/$(lsb_release -si | awk '{print tolower($0)}')/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/faucet.list
curl -L https://packagecloud.io/faucetsdn/faucet/gpgkey | apt-key add -
apt-get update
apt-get install -y faucet
mv /etc/faucet/faucet.yaml /etc/faucet/faucet.yaml.orig
cp /opt/adversarialtestingsdn/faucet.yaml /etc/faucet/faucet.yaml
systemctl daemon-reload
systemctl enable faucet
systemctl start faucet

# database setup??? (run as user rather than root)
# sudo -u ${SUDO_USER} python manage.py migrate
