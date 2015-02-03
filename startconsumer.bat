@echo off
echo "               HUEY CONSUMER"
echo "        landsatman queue processor"
echo "----------------------------------------"
echo "In another terminal, run 'python app.py'"
echo "Stop the consumer using Ctrl+C"
echo "----------------------------------------"
setlocal 
set PYTHONHOME=%VIRTUAL_ENV%\Scripts
set PATH=%PYTHONHOME%;%PATH%;%PYTHONHOME%\Lib\site-packages\huey\bin
set PYTHONPATH=.;%VIRTUAL_ENV%\Lib\site-packages;%VIRTUAL_ENV%\Lib;%VIRTUAL_ENV%\Lib
echo "----------------------------------------"
huey_consumer.py app.huey --threads=2
echo "----------------------------------------"
echo DONE
endlocal