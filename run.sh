#!/bin/bash

filename=config
cnt=0
arg=
parserinput=
parseroutput=
reviewny=
ticketny=

while read -r line
do
   tag=${line%=*}
   attr=${line#*=}
  
   case "$cnt" in
     "0") 
          if [ ! -z "$attr" ]; then
             arg="scrapy crawl stack_crawler $attr"
          else
             arg="scrapy crawl stack_crawler"
          fi;;
          #`scrapy crawl stack_crawler -a language=java -o testm.xml -s LOG_LEVEL=ERROR`;;
     "1") 
          if [ ! -z "$attr" ]; then
             arg="$arg -o ../$attr"
             parserinput="$attr"
          else
             echo "Raw output file must be set in config file"
             exit
          fi;;
     "2") 
          if [ ! -z "$attr" ]; then
             arg="$arg -s LOG_LEVEL=$attr -s LOGFILE="
          fi
          echo "Start Scrapying..."
          (cd stack && echo `$arg`)
          ;;
     "3") if [ ! -z "$attr" ]; then
             parseroutput="$attr"
          fi;;
   esac
   cnt=$((cnt+1))
done < "$filename"

while true; do
   read -p "Do you wish to make it organized in xml form?(y or n) " yn
   case $yn in
     [Yy]*) 
           if [ ! -z "$parseroutput" ] && [ ! -z "$parserinput" ]; then
              rtoxml="python rtoxml.py -i $parserinput -o $parseroutput"
              echo `$rtoxml`
           else
              echo "Failed: Need outputfile in config"
              exit
           fi
           break;;
     [Nn]*) echo "No"; break;;
         *) echo "Must be [Yy] or [Nn]";;
   esac
done

echo "Finished"

