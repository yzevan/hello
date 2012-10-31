from bs4 import BeautifulSoup
import os,sys
#wget -qO - 

soup=BeautifulSoup(open("/root/audio/npr.htm"))
transcript_list = soup.find_all('a', 'transcript')
#print transcript_list
for t in transcript_list:
	trans_url = t.get('href');
	#os.system("wget " +  mp3_url)
	#trans_file = mp3_file[0: mp3_file.rindex('mp3')] + "html"
	mp3_url = t.parent.parent.find_all('a','download')[0].get('href');
	print mp3_url
	mp3_file = mp3_url[mp3_url.rindex('/')+1: mp3_url.rindex('?')]
	print mp3_file
	os.system("wget -O " + mp3_file + " " + mp3_url)

	trans_url = t.get('href');
	trans_file = mp3_file[0: mp3_file.rindex('mp3')] + "html"
	print trans_file
	os.system("wget -O " + trans_file + " " + trans_url)

