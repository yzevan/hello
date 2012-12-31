import bs4;
from bs4 import BeautifulSoup;
import os,sys;
import urllib2;
import datetime;
"""
Download MP3 with transcript from NPR
First download the rundown.php page which includes all segment list of a specific day,
Then extract the transcript/MP3 link of those segment that have "transcript" or "Full Story" 

Sample:
<li><a class="download" href="http://pd.npr.org/anon.npr-mp3/npr/waitwait/2012/07/20120728_waitwait_04.mp3?dl=1"><span>Download</span></a></li>
<li><a class="more" href="http://www.npr.org/2012/07/28/157487495/economist-paul-krugman-plays-not-my-job">Full Story</a></li>

<li><a class="download" href="http://pd.npr.org/anon.npr-mp3/npr/waitwait/2012/07/20120728_waitwait_05.mp3?dl=1"><span>Download</span></a></li>
<li><a class="transcript" href="http://www.npr.org/2012/07/28/157506572/panel-round-two">Transcript</a></li>	     
"""


prg_list = {
        "2": "All things considered",
        "3": "Morning Edition",
        "46":"Tell me more", 
        "5": "Talk of the nation",
        "7": "Weekend Edition Saturday",
        "10": "Weekend Edition Sunday",
        "11": "Friday's show",
        "13": "Fresh Air",
        "35": "Wait wait don't tell me"
        
}

def usage():
	print "usage: {0} program_id, start_date, end_date".format(sys.argv[0])
	print "program_id list: \n"
	for key in prg_list.keys():
		print "{0}:{1} \n".format(key, prg_list[key]);
		
		
def get_audio_and_transcript(program_id, current_date):
	url = "http://www.npr.org/templates/rundowns/rundown.php?prgId={0}&prgDate={1}".format(program_id, current_date.strftime('%m-%d-%Y'));
	print url;
	soup = BeautifulSoup(urllib2.urlopen(url))
	#print soup;

	story_list = soup.find_all("div","storywrap")

	for story in story_list:		
		mp3_url = story.find('a','download').get('href');
		print mp3_url		
		mp3_file_name = mp3_url[mp3_url.rindex('/')+1: mp3_url.rindex('?')]
		print mp3_file_name
		mp3_file_path = convert_file_path(prg_list[program_id], mp3_file_name)
		                                  
		if not os.path.exists(mp3_file_path):
			file_mp3_src = urllib2.urlopen(mp3_url);
			#os.system("wget -O " + mp3_file + " " + mp3_url)			
			file_mp3 = open (mp3_file_path, 'wb')
			file_mp3.write(file_mp3_src.read())
			file_mp3.close();
		
	
		# "more" for "Full Story" link
		trans_url_node = story.find('a', ['transcript','more']);
		if trans_url_node is None:
			continue
		trans_url = trans_url_node.get('href')
		print trans_url;
		trans_file_name_prefix = mp3_file_name[0: mp3_file_name.rindex('.mp3')]
		trans_file_name = trans_file_name_prefix + "_" + trans_url[trans_url.rindex('/')+1:] + ".html"
		print trans_file_name
		
		trans_file_path = convert_file_path(prg_list[program_id], trans_file_name)
		if not os.path.exists(trans_file_path):
			soup2 = BeautifulSoup(urllib2.urlopen(trans_url))	
			transcript_node = soup2.find("div", "transcript")
			
			if transcript_node is None:
				print "No transcript in html"
				return;
		
			trans_file = open(trans_file_path, "w")
			#write css to hide disclaimer part
			trans_file.write('<style type="text/css">.disclaimer{display:none}</style>');
			trans_file.write(str(transcript_node));
			trans_file.close();

			
def convert_file_path(folder, file_name):
	"""Insert month in original file path(folder + file_name).
	For example, foler is "E:/work/" and file_name is "20121230_test.mp3",
	then return result is "E:/work/201212/20121230_test.mp3".
	if "E:/work" doesn't exist, the folder will be created."""
	month = file_name[0:6]
	
	if not os.path.exists(os.path.join(folder, month)):
		os.makedirs(os.path.join(folder, month))
	
	return os.path.join(folder,month,file_name)
		
		
def get_audio(program_id, current_date):
	url = "http://www.npr.org/templates/rundowns/rundown.php?prgId={0}&prgDate={1}".format(program_id, current_date.strftime('%m-%d-%Y'));
	print url;
	soup = BeautifulSoup(urllib2.urlopen(url))
	#print soup;
	#transcript_list = soup.find_all('a', 'transcript')
	transcript_list = soup.find_all('a', ['transcript'])
	#print transcript_list
	for t in transcript_list:		
		#os.system("wget " +  mp3_url)
		#trans_file = mp3_file[0: mp3_file.rindex('mp3')] + "html"
		mp3_url = t.parent.parent.find_all('a','download')[0].get('href');
		print mp3_url		
		mp3_file_name = mp3_url[mp3_url.rindex('/')+1: mp3_url.rindex('?')]
		print mp3_file_name	
		if not os.path.exists(os.path.join(prg_list[program_id],mp3_file_name)):
			file_mp3_src = urllib2.urlopen(mp3_url);
			#os.system("wget -O " + mp3_file + " " + mp3_url)			
			file_mp3 = open (os.path.join(prg_list[program_id], mp3_file_name),'wb')
			file_mp3.write(file_mp3_src.read())
			file_mp3.close();
		
	
		trans_url = t.get('href');
		print trans_url;
		trans_file_name_prefix = mp3_file_name[0: mp3_file_name.rindex('.mp3')]
		trans_file_name = trans_file_name_prefix + "_" + trans_url[trans_url.rindex('/')+1:] + ".html"
		print trans_file_name
		#os.system("wget -O " + trans_file + " " + trans_url)
		if not os.path.exists(os.path.join(prg_list[program_id], trans_file_name)):
			soup2 = BeautifulSoup(urllib2.urlopen(trans_url))	
			transcript_node = soup2.find("div", "transcript")
			
			if transcript_node is None:
				print "No transcript in html"
				return;
		
			trans_file = open(os.path.join(prg_list[program_id], trans_file_name), "w")
			#write css to hide disclaimer part
			trans_file.write('<style type="text/css">.disclaimer{display:none}</style>');
			trans_file.write(str(transcript_node));
			trans_file.close();
		
		
	

	
if __name__ == '__main__':
	print sys.argv;

	if len(sys.argv) != 4:
		usage();
		exit();
	program_id = sys.argv[1];
	if not os.path.exists(prg_list[program_id]):
		os.makedirs(prg_list[program_id]);
		
	start_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d');
	end_date = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%d');
	delta = datetime.timedelta(1);
	d = start_date;
	while d <= end_date:
		print d;
		get_audio_and_transcript(program_id, d);
		d += delta;
	
	print "\n It's finished!"
	
	
	
	