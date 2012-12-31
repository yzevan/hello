from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re
import os
import urllib2

"""download subtifles of TDS from officail site to official/ folder and convert it to SRT format in final/ folder """


start_id = 21
end_id = 25
season_id = 18

#URL of season17 is like season_17/episode_001/ds_17001_act1.dfxp.xml 
subtitle_url_template = "http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_{0}/episode_{1:03}/ds_{0}{1:03}_act{2}.dfxp.xml"
src_file_name_template = "ds_{0}{1:03}_act{2}.dfxp.xml"


src_folder = "official.season" + str(season_id)
dst_folder = "final.season" + str(season_id)
dst_txt_folder = "txt.season" + str(season_id)

def add_time(time1, time2):
	'''add time2 to time1.
	time1 and time2 format is like 02:00:00.123 '''
#	print "enter add_time",time1,time2
	hour1=time1.split('.')[0].split(':')[0]
	minute1=time1.split('.')[0].split(':')[1]
	second1=time1.split('.')[0].split(':')[2]
	microsecond1=time1.split('.')[1]

	hour2=time2.split('.')[0].split(':')[0]
	minute2=time2.split('.')[0].split(':')[1]
	second2=time2.split('.')[0].split(':')[2]
	microsecond2=time2.split('.')[1]

	delta1 = timedelta(0,int(second1),0,int(microsecond1),int(minute1),int(hour1))
	delta2 = timedelta(0,int(second2),0,int(microsecond2),int(minute2),int(hour2))
	d= delta1 + delta2
	h = 0
	result = "{0:02}:{1:02}:{2:02}.{3:03}".format(
	        h,d.seconds/60,d.seconds % 60,d.microseconds /1000)
#	print result
	return result


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
	
if not os.path.exists(dst_folder):
	os.mkdir(dst_folder)

if not os.path.exists(dst_txt_folder):
	os.mkdir(dst_txt_folder)
	
for id in range(start_id, end_id+1):
	#download act1 to act3 for one episode
	for act in range(1,4):
		subtitle_url = subtitle_url_template.format(season_id, id, act)
		print subtitle_url
		src_file_name = subtitle_url[subtitle_url.rindex('/')+1   :]
		
		if os.path.exists(os.path.join(src_folder, src_file_name)):
			print "file already exist! No need to download!"
			continue
		#if the file is not downloaded, download the file and save it to disk
		try:
			subtitle_response = urllib2.urlopen(subtitle_url)	
		except:
			print "Downloading issues!"
			continue
		
		
		src_file = open(os.path.join(src_folder,src_file_name), "w" )
		src_file.write(subtitle_response.read())
		src_file.close();
		
	# try to find the episode date from act1.xml
		#change file name to "YYYY-MM-DD" format
	#query first N flines 
	try:
		act1_file = open(os.path.join(src_folder,src_file_name_template.format(season_id, id, 1)),  'r')
	except:
		print "Error: act1 doesn't exist for {0}".format(id)
		continue
	
	content = ""
	#only check first 15 lines
	for j in range(1,50):
		content += act1_file.readline()
	act1_file.close()
	
	pattern = re.compile( '(January|February|March|April|May|June|July|August|Septemper|October|November|December) ([0-9]{1,2}).*(2011|2012)', re.IGNORECASE)
	result = pattern.search(content)
	if result is not None:
		month = month_dict[result.group(1).title()]
		date = result.group(2)
		year = result.group(3)
		#print month,date,year
		dst_file_name = "The.Daily.Show.{0}.{1:02}.{2:02}_ds_{3}{4:03}.srt".format(
		        int(year),
		        int(month), 
		        int(date),
		        season_id,
		        id)		
	else:
		dst_file_name = "ds_{0}{1:03}.srt".format(season_id, id)
	
	print "dst file name:" + dst_file_name
	
	dst_txt_file_name = dst_file_name + ".txt"
	
	i = 1

	dst_file = open(os.path.join(dst_folder, dst_file_name), "w")
	dst_txt_file = open(os.path.join(dst_txt_folder, dst_txt_file_name), "w")
	for act in range(1,4):			
                                 
		old_file_name = os.path.join(src_folder,
		                             src_file_name_template.format(season_id, id,act) )
		try:
			src_file = open(old_file_name, "r")
		except:
			break;
					
		soup = BeautifulSoup(src_file, "lxml")
		dst_txt_file.write(soup.get_text().encode("utf-8").title().strip())
		
		for p in soup.find_all("p"):
			if act == 1:
				act1_length = p.get("end")
			if act == 2:
				act2_length = p.get("end")

	#		print p
			if act == 1:
				new_begin = p.get("begin")
				new_end = p.get("end")
			if act == 2:
				new_begin = add_time (p.get("begin"), act1_length)
				new_end = add_time (p.get("end"), act1_length)

			if act == 3:
				new_begin = add_time (p.get("begin"), act1_length)
				new_begin = add_time( new_begin, act2_length)
				
				new_end = add_time (p.get("end"), act1_length)
				new_end = add_time( new_end, act2_length)
			dst_file.write(str(i) + "\n")
			dst_file.write("{0} --> {1}\n".format(new_begin.replace('.',','), new_end.replace('.',',')))
			dst_file.write(p.get_text().encode("utf-8").title() + "\n\n")
			i += 1
	dst_file.close()
	dst_txt_file.close()
	

'''
def add_time(time1, time2):
	hour1 = time1.split('.')[0].split(':')[0]
	minute1 = time1.split('.')[0].split(':')[1]
	second1 = time1.split('.')[0].split(':')[2]
	microsecond1 = time1.split('.')[1]

	hour2 = time1.split('.')[0].split(':')[0]
	minute2 = time1.split('.')[0].split(':')[1]
	second2 = time1.split('.')[0].split(':')[2]
	microsecond2 = time1.split('.')[1]

	delta1 = timedelta(0,int(second1), 0, int(microsecond1), int(minute1), int(hour1))
	delta2 = timedelta(0,int(second2), 0, int(microsecond2), int(minute2), int(hour2))
	d = detal1 + delta2
	result = "{0}:{1}:{2}:{3}".format(d.hours,d.minutes, d.seconds, d.microseconds)
	print result
	return result
'''	
	

def add(time1, delta):
	pass	
