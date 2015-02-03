#!/usr/bin/env python
#
# 
#
#
# Aslak Grinsted 2015
from config import settings
import re
import os
import glob
import subprocess
import re

def parsesceneid(sceneid):
	#sanitize and split sceneid 
	m = re.match(r"(?P<sensor>[A-Za-z0-9]{3,3})(?P<path>\d{3,3})(?P<row>\d{3,3})[A-Za-z0-9]{7,}", sceneid)
	sceneid = m.string[m.start():m.end()] #sanitize the sceneid 
	shortsensor=m.group('sensor')[0] + m.group('sensor')[2] #convert LC8 to L8
	url = "%s/%s/%s/%s/%s.tar.bz" % (settings['gsurl'], shortsensor, m.group('path'), m.group('row'),sceneid)

	localfilename = os.path.join(settings['targetfolder'], shortsensor, m.group('path'), m.group('row'),sceneid);

	return {'sceneid': sceneid, 'sensor': m.group('sensor'), 'path': m.group('path'), 'row': m.group('row'), 'url': url, 'localfilename': localfilename}

def isdownloaded(sceneid):
	scene=parsesceneid(sceneid)
	totalsize=0;
	for file in glob.glob(scene['localfilename'] + '*'):
		totalsize=totalsize+os.path.getsize(file)
	return totalsize > 100e6 #the compressed b8 channel is atleast 200mb for landsat8. But smaller for older satellites it might be smaller. 

def download(sceneid):
	#sceneid example = LC80080122014305LGN00
	scene=parsesceneid(sceneid)
	localfolder=os.path.split(scene['localfilename'])
	tarbzfile = scene['localfilename'] + '.tar.bz'
	if isdownloaded(sceneid): return 'OK'
	errorcode = subprocess.call(['gsutil', 'cp', '-n' , scene['url'] , scene['localfilename'] + '.tar.bz'])
	if errorcode: return 'download error'
	errorcode = subprocess.call(['tar', '-xjf', tarbzfile, '-C', localfolder]) #extract to same folder
	if errorcode: return 'untar error'
	#TODO: delete tarbzfile
	for file in glob.glob(scene['localfilename'] + '_*.TIF'):
		filepath = os.path.splitext(file)[0];
		errorcode = subprocess.call(['gdal_translate', '-co', 'COMPRESS=DEFLATE', '-co', 'tiled=yes', file, filepath+'.tiff']) #Notice extension change! -> used to detect compression so we waste time recompressing old
		if errorcode: return 'gdal_translate error' 
		#if not errorcode: os.remove(file) # TODO: delete the TIF file if compression went ok.
	return 'OK'
    #gdal_translate -co "COMPRESS=DEFLATE" -co tiled=yes "LC80080122014305LGN00_B8.TIF" "LC80080122014305LGN00_B8.tif"  %should the "TIF/tif" case be used to flag if it has been compressed. 


def searchscenes(pattern):
	matches=set() 
	for root, dir, files in os.walk(settings['targetfolder']):
	        for filename in fnmatch.filter(files, pattern):
	        	if os.path.getsize(os.path.join(root,filename))>100e6:
	        		sceneid= re.search('^[a-zA-Z0-9]+',filename).group(0);
	        		matches |= {sceneid} #Union 
	return matches


   


