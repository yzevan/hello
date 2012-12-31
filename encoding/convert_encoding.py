"""
This script is used to convert encoding of a file
"""

import os
import sys
import chardet
import cmd
import argparse

    
#----------------------------------------------------------------------
def convert(src_filename,src_encoding,  dst_encoding):
    """"""
    f = open(src_filename)
    str = f.read()
    f.close()
    
    if src_encoding is None:
        src_encoding = chardet.detect(str)['encoding']
        
    (head, ext) = os.path.splitext(src_filename)
    if ext is not None:
        dst_filename = "%s_%s.%s" % (head, dst_encoding, ext)
    else:
        dst_filename = "%s_%s" % (head, dst_encoding)
    print dst_filename    
        
    f_dst = open(dst_filename, "w")
    f_dst.write(unicode(str, src_encoding).encode(dst_encoding))
    f_dst.close()
    

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Convert encoding of a file")
    parse.add_argument('filename', metavar = 'filename', type = str, 
                       help='the source file name that needs encoding')
    parse.add_argument('encoding', help='choose the encoding method that you want convert into ')
    parse.add_argument("-s", "--src_encoding", help= 'Specify source file encoding; if not specified, auto detection will be used')
    args  = parse.parse_args();
    print args.filename
    print args.src_encoding
    convert(args.filename, args.src_encoding, args.encoding)
    
    
    