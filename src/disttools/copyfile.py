#! /usr/bin/env python

import argparse
import sys
import logging
import time
import subprocess
import re
import os

def make_dir_safe(d=None):
	if d is not None:
		if not os.path.isdir(d):
			try:
				os.makedirs(d)
			except:
				pass
		if not os.path.isdir(d):
			raise Exception('can not mkdir [%s]'%(d))

def copy_file(fromfile,tofile):
	fin = open(fromfile,'rb')
	dname = os.path.dirname(tofile)
	if len(dname) == 0:
		dname = '.'
	make_dir_safe(dname)
	fout = open(tofile,'wb')

	for l in fin:
		fout.write(l)
	fin.close()
	fout.close()
	fin = None
	fout = None
	return

def touch_file(outfile):
	with open(outfile,'wb') as fout:
		fout.write('')
	return

def trans_to_string(s):
    if sys.version[0] == '3':
        encodetype = ['UTF-8','latin-1']
        idx=0
        while idx < len(encodetype):
            try:
                return s.decode(encoding=encodetype[idx])
            except:
                idx += 1
        raise Exception('not valid bytes (%s)'%(repr(s)))
    return s


def __find_pid_win32(pid):
	cmds = 'wmic process where(ProcessId=%d) get ProcessId'%(pid)
	devnullfd = open(os.devnull,'w')
	p = subprocess.Popen(cmds,stdin=None,stdout=subprocess.PIPE,stderr=devnullfd,shell=True,env=None)
	res = False
	idx = 0
	intexpr = re.compile('^([\d]+)$')
	if p.stdout is not None:
		for line in iter(p.stdout.readline, b''):
			idx += 1
			s = trans_to_string(line)
			s = s.rstrip('\r\n')
			logging.debug('[%d][%s]'%(idx,s))
			m = intexpr.findall(s)
			if m is None or len(m) == 0:
				continue
			findpid = int(m[0])
			if findpid == pid:
				res = True
		p.stdout.close()
		p.stdout = None

	# now to wait for exit
	while True:
		if p is None:
			break
		pret = p.poll()
		if pret is not None:
			break
		time.sleep(0.1)
	p = None
	devnullfd.close()
	devnullfd = None
	return res

def __find_pid_unix_cmd(pid,cmds):
	logging.info('run cmd [%s]'%(cmds))
	devnullfd = open(os.devnull,'w')
	p = subprocess.Popen(cmds,stdin=None,stdout=subprocess.PIPE,stderr=devnullfd,shell=True,env=None)
	res = False
	intexpr = re.compile('^\s+([\d]+)\s+.*')
	idx = 0
	if p.stdout is not None:
		for line in iter(p.stdout.readline, b''):
			idx += 1
			s = trans_to_string(line)
			s = s.rstrip('\r\n')
			logging.debug('[%d][%s]'%(idx,s))
			m = intexpr.findall(s)
			if m is None or len(m) == 0:
				continue
			findpid = int(m[0])
			if findpid == pid:
				res = True
		p.stdout.close()
		p.stdout = None
	# now to wait for exit
	while True:
		if p is None:
			break
		pret = p.poll()
		if pret is not None:
			break
		time.sleep(0.1)
	p = None
	devnullfd.close()
	devnullfd = None
	return res



def find_pid(pid):
	plat = sys.platform.lower()
	if plat == 'win32':
		return __find_pid_win32(pid)
	elif plat == 'cygwin' :
		return __find_pid_unix_cmd(pid,'ps -W -e')
	elif plat == 'linux' or plat == 'linux2' or plat == 'darwin':
		return __find_pid_unix_cmd(pid,'ps -e')
	else:
		raise Exception('not support platform [%s]'%(plat))
	return False

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


def copyfile_handler(args,parser):
	set_log_level(args)
	logging.info('args %s'%(repr(args)))
	if args.pid is not None:
		# wait for this pid to wait the process to exit
		while find_pid(args.pid):
			time.sleep(0.1)
	else:
		# wait for time
		stime = time.time()
		etime = (stime + args.wait)
		ctime = stime
		while (ctime < etime):
			time.sleep((etime - ctime))
			ctime = time.time()
	# now we should copy the file
	copy_file(args.args[0],args.args[1])
	if args.touch is not None:
		touch_file(args.touch)
	sys.exit(0)
	return



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose','-v',default=0,dest='verbose',help='set verbose mode',action='count')
	parser.add_argument('--touch','-T',default=None,dest='touch',help='set touched file after copy',action='store')
	parser.add_argument('--pid','-p',default=None,dest='pid',help='specified to wait for pid to exit',type=int)
	parser.add_argument('--wait','-w',default=1.0,dest='wait',help='specify how long to wait in seconds',type=float)
	parser.add_argument('args',metavar='N',type=str,nargs=2,help='fromfile tofile')
	args = parser.parse_args()
	copyfile_handler(args,parser)
	return

if __name__ == '__main__':
	main()