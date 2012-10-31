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

    
def download(page1, page2):
    for p in range(page1, page2 + 1):
        url = "http://startingpoint.blogs.cnn.com/2012/10/page/%d" % p
        print url
        download_per_page(url)


if __name__ == "__main__":
    start_page = 1
    end_page = 25
    download(start_page, end_page)
    print("finish!")
    

