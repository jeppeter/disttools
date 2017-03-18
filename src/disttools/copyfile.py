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

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose','-v',help='set verbose mode',action='count')
	parser.add_argument('--touch','-T',help='set ')