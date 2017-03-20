#! /bin/bash


_script_file=`python -c "import sys;import os;print('%s'%(os.path.abspath(sys.argv[1])));" "$0"`
script_dir=`dirname $_script_file`
packagename=disttools

if [ -z "$PYTHON" ]
	then
	PYTHON=python
	export PYTHON
fi

$PYTHON $script_dir/pyinsert.py -i $script_dir/echo.py.tmpl pythonpython $script_dir/src/$packagename/copyfile.py | $PYTHON | $PYTHON $script_dir/pydiff.py $script_dir/src/$packagename/copyfile.py -

if [ $? -ne 0 ]
	then
	echo "pyinsert not ok" >&2
	exit 3
fi

$PYTHON $script_dir/pyinsert.py -i $script_dir/src/$packagename/__init_debug__.py.tmpl  -o $script_dir/src/$packagename/__init_debug__.py  -p '%COPYFILE_PYTHON%'   pythonpython  $script_dir/src/$packagename/copyfile.py 

if [ $? -ne 0 ]
	then
	echo "can not format" >&2
	exit 3
fi