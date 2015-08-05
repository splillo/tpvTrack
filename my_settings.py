#module for storing the files/parameters/... for the tracking code.
#Is it necessary to reload the import to re-call all functions?

import glob
import os, errno
import numpy as np
import datetime as dt

rEarth = 6370.e3 #radius of spherical Earth (m)
dFilter = 300.e3 #300.e3 #radius for whether local extremum is regional extremum
areaOverlap = .1 #fraction of tpv area overlap for determining correspondence

latThresh = 30.*np.pi/180. #segment N of this latitude
trackMinMaxBoth = 0 #0-min, 1-max (2-both shouldn't be used w/o further development)
info = '30N_mpasRegrid'

fDirData = '/raid1/nick/cases/2006/casesTable_v4.0/run/30km_20060801/'
filesData = sorted(glob.glob(fDirData+'history*.nc'), key=os.path.getmtime)
#fDirData = '/data01/tracks/summer07/eraI/'
#filesData = sorted(glob.glob(fDirData+'ERAI*.nc'), key=os.path.getmtime)
print filesData
fileMap = fDirData+'wrfout_mapProj.nc' #for inputType=wrf_trop

#time information of input data
deltaT = 6.*60.*60. #timestep between file times (s)
timeStart = dt.datetime(2006,8,1,0) #time=timeStart+iTime*deltaT
timeDelta = dt.timedelta(seconds=deltaT)
#select time intervals within filesData[iFile]...end[-1] means use all times
iTimeStart_fData = [0]
iTimeEnd_fData = [-1]
if (True): #a quick check of specified times
  nFiles = len(filesData)
  if (len(iTimeStart_fData) != nFiles or len(iTimeEnd_fData) != nFiles):
    print "Uhoh, wrong iTime*_data settings in my_settings.py"
    import sys
    sys.exit()

dateInfo = timeStart.strftime('%Y%m%d')
caseInfo = '/'+dateInfo+'/lev21/'
fDirSave = '/data02/cases/cases_table/nwp/tpvTrack/regrid/'+caseInfo; print fDirSave
#fDirSave = '/data01/tracks/wrf/algo/'
if not os.path.exists(fDirSave):
    os.makedirs(fDirSave)

#fMesh = filesData[0]  
fMesh = fDirSave+'mpas.nc'
if (('ctrl' in caseInfo) or ('kf' in caseInfo) or ('cam' in caseInfo) or ('lev21' in caseInfo)):
  fMesh = '/raid1/nick/cases/2006/casesTable_v4.0/run/30km_20060801/history.2006-08-01_00.00.00.nc'
elif ('arctic' in caseInfo):
  fMesh = '/raid1/nick/cases/2006/casesTable_v4.0/ic/arctic/init.20060801.nc'
elif ('midLat' in caseInfo):
  fMesh = '/raid1/nick/cases/2006/casesTable_v4.0/midLatMesh/ic/init.20060801.nc'
elif ('120km' in caseInfo):
  fMesh = '/raid1/nick/cases/2006/casesTable_v4.0/ic/120km/init.20060801.nc'
else:
  print 'Unknown case for mpas table of cases experiment'
  exit()
  
fMetr = fDirSave+'fields.nc'
fSeg = fDirSave+'seg.nc'
fCorr = fDirSave+'correspond_horizPlusVert.nc'
fTrack = fDirSave+'tracks_low_horizPlusVert.nc'
fMetrics = fDirSave+'metrics.nc'

inputType = 'mpasRegrid'
doPreProc = True
doSeg = True
doMetrics = True
doCorr = True
doTracks = True

def silentremove(filename):
  #from http://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
  print "Removing file (if it exists): ",filename
  try:
      os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
      if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
          raise # re-raise exception if a different error occured
