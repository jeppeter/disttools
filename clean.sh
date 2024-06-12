#! /bin/bash

if [ -z "$PYTHON" ]
	then
	export PYTHON=python
fi


_script_file=`$PYTHON -c "import sys;import os;print('%s'%(os.path.abspath(sys.argv[1])));" "$0"`
script_dir=`dirname $_script_file`
packagename=disttools

rm -rf $script_dir/dist
rm -rf $script_dir/$packagename

rm -f $script_dir/test/release/release.py.touched

rm -f $script_dir/src/$packagename/__init_debug__.pyc
rm -f $script_dir/src/$packagename/__init_debug__.py
rm -f $script_dir/test/release/release.py

rm -rf $script_dir/__pycache__/
rm -rf $script_dir/src/$packagename/__pycache__/
rm -rf $script_dir/$packagename.egg-info/

rm -f $script_dir/setup.py

