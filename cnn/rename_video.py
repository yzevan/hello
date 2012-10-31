import os
import sys
import re

search_path = "D:\\talkshow\\talking.point"

if __name__ == "__main__":
    f = open("videolist.txt")
    lines = f.read().splitlines()
    f.close()
    d = {};
    for l in lines:
        path, filename = os.path.split(l)
        patttern = re.compile('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]')
        print path,filename
        result = patttern.search(path)

        if result is not None:
            new_path = result.group()        
            print result.group()
            
            new_path = new_path.replace('/', '_')
            print new_path
            
            new_filename = new_path + "_" + filename
            d[filename] = new_filename
        else:
            print "Can't fetch date %s" % l
    
    for f in os.listdir(search_path):
        
        if d.has_key(f):
            print f, d[f]
            
            os.rename(os.path.join(search_path,f), os.path.join(search_path,d[f]))
        else:
            print "No match, filename is %s" % f
    
        
    

        #new_filename = os.path.
        #d.append({r:r})
        
    