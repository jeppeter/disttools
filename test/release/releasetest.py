#! /usr/bin/env python

import os
import sys

def _release_path_test(curpath,*paths):
    testfile = os.path.join(curpath,*paths)
    if os.path.exists(testfile):
        if curpath != sys.path[0]:
            if curpath in sys.path:
                sys.path.remove(curpath)
            oldpath=sys.path
            sys.path = [curpath]
            sys.path.extend(oldpath)
    return

def _reload_disttools_path(curpath):
	return _release_path_test(curpath,'disttools','__init__.py')

def _reload_disttools_debug_path(curpath):
	return _release_path_test(curpath,'__init_debug__.py')


topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
_reload_disttools_path(topdir)

import extargsparse
import logging
import unittest
import re
import importlib
import tempfile
import subprocess
import platform
import random
import time
from disttools import release_file,release_get_catch
from disttools import __version__ as disttools_version
from disttools import __version_info__ as disttools_version_info


test_placer_holder=True

class debug_version_test(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_A001(self):
    	verfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','VERSION')
    	vernum = '0.0.1'
    	with open(verfile,'r') as f:
    		for l in f:
    			l = l.rstrip('\r\n')
    			vernum = l
    	self.assertEqual(vernum , disttools_version)
    	sarr = re.split('\.',vernum)
    	self.assertEqual(len(sarr),3)
    	i = 0
    	while i < len(sarr):
    		sarr[i] = int(sarr[i])
    		self.assertEqual(disttools_version_info[i],sarr[i])
    		i += 1
    	return




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


def slash_string(s):
	outs =''
	for c in s:
		if c == '\\':
			outs += '\\\\'
		else:
			outs += c
	return outs


def release_handler(args,parser):
	set_log_level(args)
	global topdir
	_reload_disttools_debug_path(os.path.join(topdir,'src','disttools'))
	mod = importlib.import_module('__init_debug__')
	includes = args.release_importnames
	macros = []
	i = 0
	while i < len(args.release_macros):
		curmacros = []
		curmacros.append(args.release_macros[i])
		curmacros.append(args.release_macros[i+1])
		macros.append(curmacros)
		i += 2
	logging.info('args %s includes %s macros %s'%(repr(args),includes,macros))
	repls = dict()

	logging.info('includes %s repls %s'%(includes,repr(repls)))
	s = release_get_catch(mod,includes,macros,repls)
	outs = slash_string(s)
	releaserepls = dict()
	releasekey = 'test_placer_holder'
	releasekey += '='
	releasekey += "True"
	releaserepls[releasekey] = outs
	logging.info('releaserepls %s'%(repr(releaserepls)))
	release_file(None,args.release_output,[],[],[],releaserepls)
	sys.exit(0)
	return

def test_handler(args,parser):
	set_log_level(args)
	testargs = []
	testargs.extend(args.subnargs)
	sys.argv[1:] = testargs
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	sys.exit(0)
	return


	
def main():
	outputfile_orig = os.path.join(os.path.dirname(os.path.abspath(__file__)),'release.py')
	outputfile = slash_string(outputfile_orig)
	commandline_fmt = '''
		{
	        "verbose|v" : "+",
	        "failfast|f" : false,
	        "timewait|t" : 0.0,
	        "waitpid|w" : false,
	        "macros|m" : [],
	        "excludes|e" : [],
	        "repls|r" : [],
	        "cmdchanges|C" : [],        
			"release<release_handler>##release file##" : {
				"output|O" : "%s",
				"importnames|I" : ["debug_disttools_case"],
				"macros|M" : ["##handleoutstart","##handleoutend"]
			},
			"test<test_handler>##test mode##" : {
				"$" : "*"
			},
			"releasefile<releasefile_handler>" : {
				"$" : "+"
			}
		}
	'''
	commandline = commandline_fmt%(outputfile)
	options = extargsparse.ExtArgsOptions()
	parser = extargsparse.ExtArgsParse(options)
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	raise Exception('not supported subcommand[%s]'%(args.subcommand))
	return

if __name__ == '__main__':
	main()
