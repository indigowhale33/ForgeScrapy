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

import sys, getopt
import xml.etree.ElementTree as ET
import xml.dom.minidom
from lxml import etree

# tag and content extractor

class rtoxml:	

	def __init__(self, rawfile, outputfile):
		self.rawfile = rawfile
		self.outputfile = outputfile

	def slicing(self,argstr, tag):
		try:
			itag = '<'+tag+'>'
			etag = '</'+tag+'>'
			iidx = argstr.index(itag)
			eidx = argstr.index(etag)
			ilen = len(itag)
			target = argstr[ilen:eidx]
			retstr = argstr[eidx+len(etag):]
			return target,retstr
		except:
			print argstr
			print tag


	
	def process_raw(self):
		tree = ET.parse(self.rawfile)
		parseroot = tree.getroot()
		f = open(self.outputfile, 'w')
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

			cats=[]
			for i in item.findall('categories/value'):
				cats.append(i.text)

			if len(cats) != 0:
				rcat.text = ','.join(cats)

			lices=[]
			for i in item.findall('licenses/value'):
				lices.append(i.text)
			rlice = etree.SubElement(rmeta,"licenses")

			if len(lices) == 0:
				rlice.text = item.find('licenses').text

			if len(lices) != 0:
				rlice.text = ','.join(lices)
			rclone = etree.SubElement(rmeta,"clone")
			rclone.text = item.find('clone').text
			rtickets = etree.SubElement(rproject,"tickets")
			tic_raw_text = item.find('tickets').text

			if tic_raw_text != 'n/a':
				ticstr = tic_raw_text.encode('utf-8')

				while ticstr != "":
					tattrname, ticstr = self.slicing(ticstr, 'attr')
					tattr = etree.SubElement(rtickets, 'attr')
					tattr.text=tattrname
					while 'attr' not in ticstr[0:7] and len(ticstr) != 0:
						#print ticstr
						tstat, ticstr = self.slicing(ticstr, 'stat')
						#print tstat
						tnum, ticstr = self.slicing(ticstr, 'num')
						ttitle, ticstr = self.slicing(ticstr, 'title')
						tcreated, ticstr = self.slicing(ticstr, 'created')
						tcontent, ticstr = self.slicing(ticstr, 'main-content')

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
						
						tdiscuss, ticstr = self.slicing(ticstr, 'discussion')
						#print "tdiscuss!!!!!!!"+tdiscuss
						while tdiscuss != "":
							
							comid, tdiscuss = self.slicing(tdiscuss, 'com_id')
							comdate, tdiscuss = self.slicing(tdiscuss, 'com_date')
							comcontent, tdiscuss = self.slicing(tdiscuss, 'com-content')
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

					authors, revstr = self.slicing(revstr, 'author')
					stars, revstr = self.slicing(revstr, 'stars')
					comment, revstr = self.slicing(revstr, 'comment')
					date, revstr = self.slicing(revstr, 'date')
					rauthors.text = authors.decode('utf-8')
					rstars.text = stars.decode('utf-8')
					rcomment.text = comment.decode('utf-8')
					rdate.text = date.decode('utf-8')

		
		#print etree.tostring(root,pretty_print=True)
		f.write(etree.tostring(root,pretty_print=True))
		f.close()


def main(argv):
	inputfile=''
	outputfile=''

	try:
		opts, args = getopt.getopt(argv, "hi:o:",["help","ifile=","ofile="])
	except getopt.GetoptError:
		print 'usage: python rtoxml.py -i <inputfile> -o <outputfile>'
		sys.exit(2)

	
	for opt, arg in opts:
		if opt == '-h':
			print 'usage: python rtoxml.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i","--ifile"):
			inputfile = arg.replace('../','')
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		else:
			assert False, "unhandled option"

	if inputfile =='' or outputfile == '':
		print 'usage: python rtoxml.py -i <inputfile> -o <outputfile>'
		sys.exit()
	# if len(argv) != 2:
	# 	print 'usage: python rtoxml.py -i <inputfile> -o <outputfile>'
	# 	print "argument should be 2"
	# 	sys.exit(2)

	a = rtoxml(inputfile, outputfile)
	a.process_raw()

if __name__ == "__main__":
	main(sys.argv[1:])



# a,b = slicing('<author>gtgw</author><stars>5</stars>', 'author')
# print b	

