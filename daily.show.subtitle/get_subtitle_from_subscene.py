from bs4 import BeautifulSoup
import os,sys
#wget -qO - 

max_id = 612900
id = 612780
while id < max_id:
		print id
		#os.system("wget -O " + str(id) +" " + "\"http://v2.subscene.com/downloadissue.aspx?subtitleId=" + str(id)  + "&contentType=zip\"")
		soup = BeautifulSoup(open(str(id)))
		#print soup
		href = soup.find_all('a', '#s_lc_bcr_downloadlink')
		h2 = soup.select('a#s_lc_bcr_downloadlink')
	
		subtitle_url = h2[0].get('href')
		#href = soup.find('a','#s_lc_bcr_downloadlink')
		#print href
		os.system("wget " + "\"http://v2.subscene.com" + subtitle_url + "\"")
		id += 1
		

#soup=BeautifulSoup(open("/root/audio/npr.htm"))
#transcript_list = soup.find_all('a', 'transcript')
