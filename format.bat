echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF
set packagename=disttools

if -%PYTHON%- == -- (
	set PYTHON=python
)


%PYTHON% %script_dir%pyinsert.py -i %script_dir%echo.py.tmpl pythonpython %script_dir%src\%packagename%\copyfile.py | %PYTHON% | %PYTHON% %script_dir%pydiff.py %script_dir%src\%packagename%\copyfile.py -

if NOT %errorlevel% == 0 (
	echo "can not make copyfile" 
	goto :error
)

%PYTHON% %script_dir%pyinsert.py -i %script_dir%src\%packagename%\__init_debug__.py.tmpl  -o %script_dir%src\%packagename%\__init_debug__.py  -p "%%COPYFILE_PYTHON%%"   pythonpython  %script_dir%src\%packagename%\copyfile.py 

goto :exitcode

:error
exit /b %errorlevel%

:exitcode
echo "format success"