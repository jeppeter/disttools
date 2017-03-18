#! /usr/bin/env python

import extargsparse
import sys
import logging

def __get_python_python(s):
	outs = ''
	for c in s:
		if c == '\'':
			outs += '\\\''
		elif c == '\\':
			outs += '\\\\'
		elif c == '\r':
			outs += '\\r'
		else:
			outs += c
	return outs

def read_file(infile=None):
	rets = ''
	fin = sys.stdin
	if infile is not None:
		fin = open(infile,'rb')
	bmode = False
	if 'b' in fin.mode:
		bmode = True
	for l in fin:
		if sys.version[0] == '2' or not bmode:
			rets += l
		else:
			# not binary mode ,so we should make decode for 
			rets += l.decode(encoding='UTF-8')

	if fin != sys.stdin:
		fin.close()
	fin = None
	return rets

def write_file(s,outfile=None):
	fout = sys.stdout
	if outfile is not None:
		fout = open(outfile,'wb')
	bmode = False
	if 'b' in fout.mode:
		bmode = True
	if sys.version[0] == '2' or not bmode:
		fout.write(s)
	else:
		fout.write(s.encode(encoding='UTF-8'))
	if fout != sys.stdout:
		fout.close()
	fout = None
	return


def pythonpython_handler(args,parser):
	repls = ''
	for f in args.subnargs:
		repls += read_file(f)
	repls = __get_python_python(repls)
	outs = read_file(args.input)
	outs = outs.replace(args.pattern,repls)
	write_file(outs,args.output)
	sys.exit(0)
	return

def main():
	commandline='''
	{
		"verbose|v" : "+",
		"pattern|p" : "%REPLACE_PATTERN%",
		"input|i" : null,
		"output|o" : null,
		"pythonpython<pythonpython_handler>" : {
			"$" : "*"
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line(None,parser)
	raise Exception('[%s] not supported'%(args.subcommand))
	return

if __name__ == '__main__':
	main()