"""
Monitor a directory for text files that contain given text.
"""

__author__ = 'jayaimzzz'

import argparse
import os
import time
import signal
import logging

run_flag = True 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(message)s')
file_handler = logging.FileHandler("filelog.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# logging.basicConfig(filename="filelog.log", level=logging.INFO, format='%(asctime)s:%(message)s')

def handle_signal(signum, stack):
    logger.info("Signal number: {}".format(signum))
    global run_flag
    run_flag = False

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def watch_dirs(args, dict1):
    '''check directory once for changes'''
    ext = 'txt' if args.ext == None else args.ext
    dir1, magic_text = args.dir, args.magic
    try:
        files = [file for file in os.listdir(dir1) if file.endswith(ext)]
    except:
        logger.info('the directory "{}" is not found'.format(dir1))
    else:
        for file in files:
            if file not in dict1:
                dict1[file] = -1
                logger.info('file "{}" added'.format(file))
            with open(dir1 + "/" + file) as text:
                for i, line in enumerate(text):
                    if dict1[file] < i:
                        dict1[file] = i
                        if magic_text in line:
                            logger.info('"{}" found in "{}" at line {}'.format(magic_text,file,i + 1))
        removed_files = []
        for key in dict1:
            if key not in files:
                logger.info('"{}" file was deleted'.format(key))
                removed_files.append(key)
        if removed_files:
            for file in removed_files:
                dict1.pop(file)

def main(args):
    '''Polls the watch_dir function at the declared interval'''
    logger.info('Started watching directory "{}"'.format(args.dir))
    int1 = 1 if args.int == None else args.int 
    dict1 = {}
    while run_flag:
        try:
            watch_dirs(args, dict1)
        except:
            logger.exception("exception on main")     
        time.sleep(int1)
    logger.info("Thank you for dir watching. Goodbye")

def create_parser():
    '''returns an arguments parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", help="directory to monitor", required=True)
    parser.add_argument("-magic", help="the text to monitor for", required=True)
    parser.add_argument("-ext", help="the file extension to monitor")
    parser.add_argument("-int", help="the polling interval in seconds")
    return parser

if __name__ == '__main__':
    '''What is this docstring for?'''
    parser = create_parser()
    args = parser.parse_args()
    main(args)