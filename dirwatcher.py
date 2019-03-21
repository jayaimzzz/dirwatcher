"""
Monitor a directory for text files that contain given text.
"""

__author__ = 'jayaimzzz'

import argparse
import os
import time
import signal

run_flag = True 

def handle_signal(signum, stack):
    print "inside handle_signal"
    run_flag = False
    # raise SystemExit("exiting")

signal.signal(signal.SIGINT, handle_signal)


def main(args):
    ext = 'txt' if args.ext == None else args.ext
    int1 = 2 if args.int == None else args.int
    dir1, magic_text = args.dir, args.text
    dict1 = {}

    while run_flag:
        print run_flag
        try:
            files = os.listdir(dir1)
        except:
            print 'the directory "{}" is not found'.format(dir1)
        else:
            for file in files:
                if file not in dict1:
                    dict1[file] = -1
                    print 'file "{}" added'.format(file)
                with open(dir1 + "/" + file) as text:
                    for i, line in enumerate(text):
                        if dict1[file] < i:
                            dict1[file] = i
                            if magic_text in line:
                                print '"{}" found in "{}" at line {}'.format(magic_text,file,i + 1)
            removed_files = []
            for key in dict1:
                if key not in files:
                    print '{} file was deleted'.format(key)
                    removed_files.append(key)
            if removed_files:
                for file in removed_files:
                    dict1.pop(file)
        time.sleep(int1)
    print "stop now"


                

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="directory to monitor")
    parser.add_argument("text", help="the text to monitor for")
    parser.add_argument("-ext", help="the file extension to monitor")
    parser.add_argument("-int", help="the polling interval in seconds")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)