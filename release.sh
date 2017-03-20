#! /bin/bash

_script_file=`python -c "import os;import sys;sys.stdout.write('%s'%(os.path.realpath(sys.argv[1])))" $0`
script_dir=`dirname $_script_file`
packagename=disttools

if [ -z "$PYTHON" ]
	then
	export PYTHON=python
fi

wait_file_until()
{
	_waitf="$1"
	_maxtime=100
	_checked=0
	if [ $# -gt 1 ]
		then
		_maxtime=$2
	fi
	_cnt=0
	while [ 1 ]
	do
		if [ -f "$_waitf" ]
			then
			if [ $_checked -gt 3 ]
				then
				rm -f "$_waitf"
				break
			fi
			/bin/echo  "import time;time.sleep(0.1)" | $PYTHON
			_checked=`expr $_checked \+ 1`
		else
			_checked=0
			/bin/echo "import time;time.sleep(0.1)" | $PYTHON	
			_cnt=`expr $_cnt \+ 1`
			if [ $_cnt -gt $_maxtime ]
				then
				/bin/echo "can not wait ($_waitf)" >&2
				exit 3
			fi
		fi
	done	
}

rm -f $script_dir/$packagename/__init__.py.touched 
rm -f $script_dir/test/release/release.py.touched


$PYTHON $script_dir/pyinsert.py -i $script_dir/echo.py.tmpl pythonpython $script_dir/src/$packagename/copyfile.py  | $PYTHON | $PYTHON pydiff.py - $script_dir/src/$packagename/copyfile.py
if [ $? -ne 0 ]
	then
	echo "can not pyinsert ok" >&2
	exit 3
fi 

$PYTHON $script_dir/pyinsert.py -i $script_dir/src/$packagename/__init_debug__.py.tmpl -o $script_dir/src/$packagename/__init_debug__.py -p '%COPYFILE_PYTHON%' pythonpython $script_dir/src/$packagename/copyfile.py

$PYTHON $script_dir/src/$packagename/__init_debug__.py test
if [ $? -ne 0 ]
	then
	echo "__init_debug__ test not ok" >&2
	exit 3
fi

$PYTHON $script_dir/make_setup.py

$PYTHON $script_dir/src/$packagename/__init_debug__.py release
wait_file_until "$script_dir/$packagename/__init__.py.touched"


$PYTHON $script_dir/test/release/releasetest.py release
wait_file_until "$script_dir/test/release/release.py.touched"

$PYTHON $script_dir/test/release/release.py test
if [ $? -ne 0 ]
	then
	/bin/echo "can not run ok" >&2
	exit 3
fi
