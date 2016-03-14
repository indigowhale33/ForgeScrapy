# ForgeCloner

* author: GwonJae Cho
* Deleted the spider file which contains the main functional code. Exclusive for the research of Chris Vendome.
* Contribution for research of Chris Vendome, Ph.D Candidate at William and Mary
* 
First in the ForgeCloner folder, install the prerequisites which include python-dev, scrapy etc. by
```
$chmod 755 install.sh
$./install.sh
```

Then edit the config file for your favor(the format is described at the bottom)

Finally simply run by
```
$./run.sh
```

##Log file
Log file is located in Forgecloner named observe.log.


##Formats

####Usage:
![alt text](https://github.com/cvendome/ForgeCloner/blob/master/image/usage.png "Usage")
####Example:
parse java based projects each with reviews and tickets, and number of parsing ticket limit is 10000.
```
arg=-a language=java -a review=y -a ticket=y -a tlimit=10000
rawoutput=raw.xml
loglevel=ERROR
outputfile=refined.xml
```

####Output XML Structure:
![alt text](https://github.com/cvendome/ForgeCloner/blob/master/image/xmlformat.png "XmlFormat")


