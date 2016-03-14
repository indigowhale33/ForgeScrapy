#!/bin/bash

function helper-script(){
   #cat > $1
   chmod 755 $1
}

cat <<PACKAGES | xargs sudo apt-get install $APTITUDE_OPTIONS
python-dev
build-essential
python-pip
PACKAGES

cat <<SCRAPY | xargs pip install
scrapy
SCRAPY

helper-script run.sh
