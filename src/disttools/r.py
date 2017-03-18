#! /usr/bin/env python

import extargsparse
import sys
import os
import time
import subprocess

def run_cmd(args):
	cmd = ''
	for c in args:
		if len(cmd) > 0:
			cmd += ' '
		cmd += '"%s"'%(c)
	subprocess.Popen(cmd,shell=True,stdout=None,stderr=None,stdin=None)
	return

def main():
	commandline='''
	{
		"verbose|v" : "+",
		"time|t" : 0.0,
		"pid|p" : false,
		"$" : "*"
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	if args.pid and len(args.args) > 2:
		args.args.insert(2,'%d'%(os.getpid()))
		args.args.insert(2,'--pid')
	run_cmd(args.args)
	if (args.time - 0.0) > 0.0001:
		time.sleep(args.time)
	sys.exit(0)
	return

main()

