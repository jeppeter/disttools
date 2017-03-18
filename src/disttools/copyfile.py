#! /usr/bin/env python

import argparse
import sys
import os
import logging
import time

def copy_file(args,fromfile,tofile):
	fin = open(fromfile,'rb')
	fout = open(tofile,'wb')

	for l in fin:
		if sys.version[0] == '2':
			fout.write(l)
		else:
			fout.write(l)
	fin.close()
	fout.close()
	fin = None
	fout = None
	return

def touch_file(args,outfile):
	with open(outfile,'wb') as fout:
		fout.write('')
	return

def __find_pid_win32(pid):

def find_pid(pid):
	plat = sys.platform.lower()
	if plat == 'win32':
		return __find_pid_win32(pid)
	elif plat == 'cygwin':
		return __find_pid_cygwin(pid)
	elif plat == 'linux' or plat == 'linux2':
		return __find_pid_linux(pid)
	elif plat == 'darwin':
		return __find_pid_darwin(pid)
	else:
		raise Exception('not support platform [%s]'%(plat))
	return False

def copyfile_handler(args):
	if args.pid is not None:
		# wait for this pid to wait

	else:
		# wait for time
		stime = time.time()
		etime = (stime + args.wait)
		ctime = stime
		while (ctime < etime):
			time.sleep((etime - ctime))
			ctime = time.time()

def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose','-v',default=0,dest='verbose',help='set verbose mode',action='count')
	parser.add_argument('--touch','-T',default=None,dest='touch',help='set touched file after copy',action='store')
	parser.add_argument('--pid','-p',default=None,dest='pid',help='specified to wait for pid to exit',type=int)
	parser.add_argument('--wait','-w',default=1.0,dest='wait',help='specify how long to wait in seconds',type=float)
	parser.add_argument('args',metavar='N',type=str,nargs=2,help='fromfile tofile')
	args = parser.parse_args()
	set_log_level(args)
	logging.debug('args %s'%(repr(args)))
	return

if __name__ == '__main__':
	main()