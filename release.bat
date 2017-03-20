echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF
set packagename=disttools

if -%PYTHON%- == -- (
	set PYTHON=python
)


%PYTHON% %script_dir%pyinsert.py -i %script_dir%echo.py.tmpl pythonpython %script_dir%src\%packagename%\copyfile.py | %PYTHON% | %PYTHON% %script_dir%pydiff.py %script_dir%src\%packagename%\copyfile.py -

if NOT %errorlevel% == 0 (
	echo "can not make copyfile" >&2
	goto :error
)



%PYTHON% %script_dir%pyinsert.py -i %script_dir%src\%packagename%\__init_debug__.py.tmpl  -o %script_dir%src\%packagename%\__init_debug__.py  -p "%%COPYFILE_PYTHON%%"   pythonpython  %script_dir%src\%packagename%\copyfile.py 

%PYTHON% %script_dir%src\%packagename%\__init_debug__.py test
if NOT %errorlevel% == 0 (
	echo "can not test for __init_debug__" 
	goto :error
)


%PYTHON% %script_dir%make_setup.py

%PYTHON% %script_dir%src\%packagename%\__init_debug__.py release
call :check_file %script_dir%%packagename%\__init__.py.touched

%PYTHON% %script_dir%test\release\releasetest.py release --release-output %script_dir%test\release\release.py
call :check_file %script_dir%test\release\release.py.touched


goto :exitcode


:check_file

set _waitf=%1
set _maxtime=100
set _cnt=0
set _checked=0
if x%_waitf% == x (
	goto :check_file_end
)

:check_file_again
if %_maxtime% LSS %_cnt% (
	echo "can not wait (%_waitf%) in (%_maxtime%)"
	exit /b 3
)

if exist %_waitf% (
	python -c "import time;time.sleep(0.1)"
	set /A _checked=%_checked%+1
	if %_checked% GTR 3 (
		del /F /Q %_waitf%
		goto :check_file_end
	)
    echo "will check (%_checked%) %_waitf%"
) else (
	set _checked=0
)

set /A _cnt=%_cnt%+1
%PYTHON% -c "import time;time.sleep(0.1)"
goto :check_file_again

:check_file_end
exit /b 0


:error
exit /b %errorlevel%

:exitcode
%PYTHON% %script_dir%test\release\release.py test 
set res=%errorlevel%
if -%res%- == -0- (
	echo "release ok"
) else (
	echo "not run test ok"
	exit /b 3
)


echo on