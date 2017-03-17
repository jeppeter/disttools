#! /usr/bin/env python

import sys
import os


def diff_file(afp,bfp):
	als = afp.readlines()
	bls = bfp.readlines()

	if len(als) != len(bls):
		sys.stderr.write('[%d] != [%d]\n'%(len(als),len(bls)))
		return False
	i = 0
	while i < len(als):
		al = als[i]
		bl = bls[i]
		if sys.version[0] != '2':
			if isinstance(al,bytes):
				al = al.decode(encoding='UTF-8')
			if isinstance(bl,bytes):
				bl = bl.decode(encoding='UTF-8')
		if al != bl:
			sys.stderr.write('[%d] %s => %s'%(i,al.rstrip('\r\n'),bl.rstrip('\r\n')))
			return False
		i += 1
	return True


def main():
	if len(sys.argv[1:]) < 1:
		raise Exception('at least one ')

	afile = sys.argv[1]
	bfile = '-'
	if len(sys.argv[1:]) > 1:
		bfile = sys.argv[2]

	if afile != '-':
		afile = os.path.realpath(afile)

	if bfile != '-':
		bfile = os.path.realpath(bfile)
	if afile == bfile:
		raise Exception('afile [%s] is the same [%s]'%(afile,bfile))
	afp = sys.stdin
	bfp = sys.stdin
	if afile != '-':
		afp = open(afile,'rb')
	if bfile != '-':
		bfp = open(bfile,'rb')

	bsame = diff_file(afp,bfp)

	if afp != sys.stdin:
		afp.close()
	if bfp != sys.stdin:
		bfp.close()
	afp = None
	bfp = None
	if bsame :		
		sys.exit(0)
	sys
	sys.exit(1)
	return

if __name__ == '__main__':
	main()