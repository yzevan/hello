''' Download transcripts(XML format) from HBO offcial site and convert it into TXT'''

from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re
import os
import urllib2
import re



start_id = 283
end_id = 300

#URL of season17 is like episode_001/ds_17001_act1.dfxp.xml 
quotes_url_template = "http://render.cdn.hbo.com/data/content/real-time-with-bill-maher/episodes/0/{0}-episode/synopsis/quotes.xml?g=n"
newrule_url_template = "http://render.cdn.hbo.com/data/content/real-time-with-bill-maher/episodes/0/{0}-episode/article/new-rules.xml?g=n"
src_file_name_template = "ds_18{0:03}_act{1}.dfxp.xml"


src_folder = "official"

dst_txt_folder = "txt"




month_dict = {"January":1, 
		"February":2,
		"March":3, 
		"April":4,
		"May":5,
		"June":6,
		"July":7,
		"August":8,
		"September":9,
		"October":10,
		"November":11,
		"December":12};





#offical/ folder stores original subtitle, ./final/ folder stores converted SRT subtitle
if not os.path.exists(src_folder):
	os.mkdir(src_folder)
	
if not os.path.exists(dst_txt_folder):
	os.mkdir(dst_txt_folder)
	
for id in range(start_id, end_id+1):
	
	#download new rule xml
	newrule_url = newrule_url_template.format(id)
	src_file_name = str(id) + ".newrule.xml"
	if os.path.exists(os.path.join(src_folder, src_file_name)):
		print "file already exist! No need to download!"
		
		#if the file is not downloaded, download the file and save it to disk
	else:
		try:
			print "Trying to get New Rule script for episode %d" % id
			newrule_response = urllib2.urlopen(newrule_url)	
			newrule_response_text = newrule_response.read()
			
			if BeautifulSoup(newrule_response_text).find("title").get_text().startswith("404"):
				print "404 error!\n"
				continue	
			
			src_file = open(os.path.join(src_folder,src_file_name), "w" )
			src_file.write(newrule_response_text)
			src_file.close();
			
		except Exception, e:
			print "Downloading issues!" % e
			continue
	
		
	soup = BeautifulSoup(open(os.path.join(src_folder,src_file_name)), "xml" )
	
	title = soup.find("title").get_text()
	print "title is:" + title
	print "search is:" + soup.find("search").get_text()
	print "try to match date..."
	
	pattern = re.compile( '(January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{1,2}).*([0-9]{4})', re.IGNORECASE)
	result = pattern.search(title)
	if result is not None:
		month = month_dict[result.group(1).title()]
		date = result.group(2)
		year = result.group(3)
		match_date = "%s_%s_%s" % (year, month, date)
		print "Match date %s_%s_%s" % (year, month, date)

	else:
		match_date = ""
		print "Can't match date!"		

	dst_file_name = str(id) + "." + match_date +  ".newrule.html"
	dst_file = open(os.path.join(dst_txt_folder, dst_file_name), "w")	

	for article in soup.find_all("article"):
		dst_file.write(article.get_text().encode("utf-8"))
	dst_file.close()		

	#download quotes xml
	quotes_url = quotes_url_template.format(id)
	print quotes_url
	src_file_name = str(id) + ".quotes.xml"
	if os.path.exists(os.path.join(src_folder, src_file_name)):
		print "file already exist! No need to download!"
	else:	
	#if the file is not downloaded, download the file and save it to disk
		try:
			quotes_response = urllib2.urlopen(quotes_url)	
			src_file = open(os.path.join(src_folder,src_file_name), "w" )
			src_file.write(quotes_response.read())
			src_file.close();			
		except:
			print "Downloading issues!"
			continue

	
	dst_file_name = str(id) +"." + match_date +  ".quotes.html"
	dst_file = open(os.path.join(dst_txt_folder, dst_file_name), "w")	
	soup = BeautifulSoup(open(os.path.join(src_folder,src_file_name)), "xml" )
	
	for article in soup.find_all("article"):
		dst_file.write(article.get_text().encode("utf-8"))
	dst_file.close()
	
	
	
	
	
	print "\n"	
