###################################################################
# XML structure #
#################
#
# <Projects>
#  |--<Project>
#      |--<meta>
#      |   |--<title>      : project title
#      |   |--<url>        : project url
#      |   |--<stars>      : project overall rating stars(?/5stars)
#      |   |--<downloads>  : number of downloads in this week
#      |   |--<categories> : categories
#      |   |--<licenses>   : licenses
#      |   |--<clone>      : clone url('no clone' if not exist)
#      |   |--<tickets>    : tickets  ('n/a' if not exist)
#      |       |--<attr>   : ticket category(bug/feature request/issue etc.)
#      |          |--<issue>      : one ticket/issue
#      |              |--<title>  : ticket/issue title
#      |              |--<num>    : ticket/issue number
#      |              |--<stat>   : ticket status(open/close)
#      |              |--<created> : ticket created
#      |--<reviews>
#          |--<review>
#              |--<review-author>   : reviewer's id
#              |--<review-stars>    : review rating stars
#              |--<review-comment>  : review comment(content)
#              |--<review-date>     : review post date
#
#
#########################################################################


import xml.etree.ElementTree as ET
import xml.dom.minidom
from lxml import etree

# tag and content extractor
def slicing(argstr, tag):
	itag = '<'+tag+'>'
	etag = '</'+tag+'>'
	iidx = argstr.index(itag)
	eidx = argstr.index(etag)
	ilen = len(itag)
	target = argstr[ilen:eidx]
	retstr = argstr[eidx+len(etag):]
	return target,retstr


tree = ET.parse('test.xml')
parseroot = tree.getroot()

f = open('testt.xml', 'w')
root = etree.Element("Projects")




for item in parseroot:

	rproject = etree.SubElement(root,"Project")
	rmeta = etree.SubElement(rproject,"meta")
	rtitle = etree.SubElement(rmeta,"title")
	rtitle.text = item.find('title').text
	rurl = etree.SubElement(rmeta,"url")
	rurl.text = item.find('url').text
	rstars = etree.SubElement(rmeta,"stars")
	rstars.text = item.find('stars').text
	rdownloads = etree.SubElement(rmeta,"downloads")
	rdownloads.text = item.find('downloads').text
	rcat = etree.SubElement(rmeta,"categories")
	rcat.text = item.find('categories').text
	rlice = etree.SubElement(rmeta,"licenses")
	if rlice.text is not None:
		rlice.text = item.find('licenses').text
	rclone = etree.SubElement(rmeta,"clone")
	rclone.text = item.find('clone').text
	rtickets = etree.SubElement(rproject,"tickets")
	tic_raw_text = item.find('tickets').text

	if tic_raw_text != 'n/a':
		ticstr = tic_raw_text.encode('utf-8')

		while ticstr != "":
			tattrname, ticstr = slicing(ticstr, 'attr')
			tattr = etree.SubElement(rtickets, 'attr')
			tattr.text=tattrname
			while 'attr' not in ticstr[0:7] and len(ticstr) != 0:
				#print ticstr
				tstat, ticstr = slicing(ticstr, 'stat')
				#print tstat
				tnum, ticstr = slicing(ticstr, 'num')
				ttitle, ticstr = slicing(ticstr, 'title')
				tcreated, ticstr = slicing(ticstr, 'created')
				tcontent, ticstr = slicing(ticstr, 'main-content')

				ttitle = ttitle.decode('utf-8')
				tcreated = tcreated.decode('utf-8')
				tnum = tnum.decode('utf-8')
				tstat = tstat.decode('utf-8')

				tissue = etree.SubElement(tattr,"issue")
				tissue.text = tcontent.decode('utf-8')

				tsubtitle = etree.SubElement(tissue,"title")
				tsubnum = etree.SubElement(tissue,"num")
				tsubstat = etree.SubElement(tissue,"stat")
				tsubcreated = etree.SubElement(tissue,"created")

				tsubtitle.text = ttitle
				tsubnum.text = tnum
				tsubstat.text = tstat
				tsubcreated.text = tcreated
				
				tdiscuss, ticstr = slicing(ticstr, 'discussion')
				#print "tdiscuss!!!!!!!"+tdiscuss
				while tdiscuss != "":
					
					comid, tdiscuss = slicing(tdiscuss, 'com_id')
					comdate, tdiscuss = slicing(tdiscuss, 'com_date')
					comcontent, tdiscuss = slicing(tdiscuss, 'com-content')
					tcomtree = etree.SubElement(tissue,"disc-comment")
					tcomid = etree.SubElement(tcomtree,"d_comment_id")
					tcomdate = etree.SubElement(tcomtree,"d_comment_date")
					tcomcontent = etree.SubElement(tcomtree,"d_comment_content")
					tcomid.text = comid.decode('utf-8')
					tcomdate.text = comdate.decode('utf-8')
					tcomcontent.text = comcontent.decode('utf-8')

	rreviews = etree.SubElement(rproject,"reviews")

	reviews = item.find('reviews')
	if reviews.text is not None:
		revstr = reviews.text.encode('utf-8')
		while revstr:
			rreview = etree.SubElement(rreviews,"review")
			rauthors = etree.SubElement(rreview,"review-author")
			rstars = etree.SubElement(rreview,"review-stars")
			rcomment = etree.SubElement(rreview,"review-comment")
			rdate = etree.SubElement(rreview,"review-date")

			authors, revstr = slicing(revstr, 'author')
			stars, revstr = slicing(revstr, 'stars')
			comment, revstr = slicing(revstr, 'comment')
			date, revstr = slicing(revstr, 'date')
			rauthors.text = authors.decode('utf-8')
			rstars.text = stars.decode('utf-8')
			rcomment.text = comment.decode('utf-8')
			rdate.text = date.decode('utf-8')

f.close()
print etree.tostring(root,pretty_print=True)



# a,b = slicing('<author>gtgw</author><stars>5</stars>', 'author')
# print b	