import sys,os
import urllib2
import re


def download_per_page(url):
    f = urllib2.urlopen(url)
    content = f.read()
    #print content
    pattern = re.compile("cnnLoadPLayer\('(.*?)'")
    #result = pattern.search(content)
    result = pattern.findall(content)
    #print result
    if result:
        f = open("./videolist.txt", "a")        
        for r in result:
            print "http://ht.cdn.turner.com/cnn/big//" + r + "_640x360_dl.flv"
            f.write("http://ht.cdn.turner.com/cnn/big//" + r + "_640x360_dl.flv" +"\n")
        f.close()

    


#----------------------------------------------------------------------
def download_by_month(year, month):
    """get all the download links of one month"""
    page = 1
    while True:
        url = "http://startingpoint.blogs.cnn.com/%d/%d/page/%d" % (year, month, page)
        print url
        try:
            download_per_page(url)
            page = page + 1
        except urllib2.HTTPError, e:
            print e
            if e.code == 404:
                break
            return
        
    
        

if __name__ == "__main__":
    year = 2012
    month = 12
    download_by_month(year, month)
    print("finish!")
    

