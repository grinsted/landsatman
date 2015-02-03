#!/bin/bash

echo "               HUEY CONSUMER"
echo "        landsatman queue processor"
echo "----------------------------------------"
echo "In another terminal, run 'python app.py'"
echo "Stop the consumer using Ctrl+C"
echo "----------------------------------------"
OLDPYPATH=$PYTHONPATH
export PYTHONPATH=$(echo ".:$PYTHONPATH" | awk -v RS=: -v ORS=: '!(a[$0]++)' | sed 's/:+$//')  #this is just to remove duplicates
PATH=$PATH:$VIRTUAL_ENV/lib/python2.7/site-packages/huey/bin
echo "----------------------------------------"
huey_consumer.py app.huey --threads=2
echo "----------------------------------------"
export PYTHONPATH=$OLDPYPATH
echo DONE