from bs4 import BeautifulSoup
from urllib2 import urlopen

#package_list = urlopen("http://pypi.python.org/pypi?%3Aaction=index")
soup_package_list = BeautifulSoup(open("python_index.html","r"))

result_file = open("result.txt", "w")

for a in soup_package_list.find_all('table', 'list')[0].find_all('a'):
	#if file exist, read from it
#	package_file_name = 
	package_desc = a.parent.find_next_sibling()
	package_link = "http://pypi.python.org" + a.get("href")
	package_file_name = "all_package/" + a.get("href").replace('/','_')
	print package_link
	try :
		f = open(package_file_name, 'r')
		soup_package = BeautifulSoup(f)
	except : 	#if file doesn't exit, get it from web, save it into file 
		f = open(package_file_name, 'w')
		try:
			f_url =urlopen(package_link)
		except:
			print "error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"	
			continue
		str = f_url.read()
		f.write(str)
		f.close
		soup_package = BeautifulSoup(str)

	row = soup_package.find("tr", "odd");
	if row <> None:
		for c in row.findChildren(None,{},False):                        
#		    print c.get_text() + ":";
		    result_file.write( c.get_text().replace('\n','').replace('\t','').replace(' ','') + ":" )
		result_file.write(package_desc.get_text().encode('UTF-8'))
		result_file.write("\n")
