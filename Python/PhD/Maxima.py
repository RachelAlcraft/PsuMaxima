#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      04/05/2020
Function:  Calls to an external C++ program
Description: 
============
This calls out to an external C++ program with some data entered purely for inout/output testing
The return of this external program is a csv style stream
There is code commented out that can be used in testing outside of the cgi server environment
"""

#************************************************************************************************

import subprocess as sub
import pandas as pd
from io import StringIO as sio

def getFile(filename, url):
  import urllib.request
  urllib.request.urlretrieve(url,filename)

def getCsvFromCppResults(cppResults,ID):
  startPos = cppResults.find('BEGIN_' + ID) + len('BEGIN_' + ID)
  endPos = cppResults.find('END_' + ID)
  if endPos > startPos:
    exe_result = cppResults[startPos:endPos]    
    exe_data = sio(exe_result)
    df = pd.read_csv(exe_data)
    return df
  else:
    #print(startPos,endPos)
    return pd.DataFrame()
  
def doWeHaveAllFiles(pdbCode):
  done = True
  import os
  directory = '/d/projects/u/ab002/Thesis/PhD/Data/'
  allFiles = True
  #Files from the PDBE	
  origPdb = directory + 'Pdb/pdb' + pdbCode + '.ent'
  ccp4File = directory + 'Ccp4/' + pdbCode + '.ccp4'
  ccp4Diff = directory + 'Ccp4/' + pdbCode + '_diff.ccp4'

  if not os.path.isfile(origPdb):
    #print('getting pdb file from pdb</br>')    
    getFile(origPdb,'https://www.ebi.ac.uk/pdbe/entry-files/download/pdb' + pdbCode + '.ent')

  if not os.path.isfile(ccp4File):
    #print('getting ccp4 files from pdb</br>')    
    getFile(ccp4File,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode + '.ccp4')
    getFile(ccp4Diff,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode +'_diff.ccp4')

  # Files to calculate
  adjPdb = directory + 'Adjusted/pdb' + pdbCode + '.ent'
  peaksFile = directory + 'Peaks/' + pdbCode + '_Maxa.csv'
  report =  directory + 'Report/MaximaDifferences_' + pdbCode + '.csv'

  return done

def runCppModule(pdb, cX,cY,cZ,lX,lY,lZ,pX,pY,pZ):    
    commandlinePeaks = "PEAKS|" + pdb + "|"
    commandlinePeaks += str(cX) + "_" + str(cY) + "_" + str(cZ) + "|"
    commandlinePeaks += str(lX) + "_" + str(lY) + "_" + str(lZ) + "|"
    commandlinePeaks += str(pX) + "_" + str(pY) + "_" + str(pZ)

    commandlineDensity = "DENSITY|" + pdb + "|"
    #Baffling, 6jvv only fails if I add more into the command line
    #commandlineDensity += str(cX) + "|" + str(cY) + "|" + str(cZ) + "|
    #commandlineDensity += str(lX) + "-" + str(lY) + "-" + str(lZ) + "|"
    #commandlineDensity += str(pX) + "-" + str(pY) + "-" + str(pZ)
    
    #try:
    if True:
      ### CALL PEAKS ###
      pig =  sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlinePeaks], stdout=sub.PIPE)
      result = pig.communicate(input=b"This is sample text.\n")
      exe_result = str(result[0],'utf-8')
      pig.kill()
      #####################################################
      #print(exe_result)
      dfInputs = getCsvFromCppResults(exe_result, 'USERINPUTS')
      #print(dfInputs)
      df1 = getCsvFromCppResults(exe_result, 'ALLPEAKS')
      if len(df1) == 0:
        print("results from exe=",result)
        return []      
      df2 = getCsvFromCppResults(exe_result, 'ATOMPEAKS')
      df3 = getCsvFromCppResults(exe_result, 'ATOMDENSITY')

      ### CALL DENSITY AND SLICES ###
      
      pigD = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlineDensity], stdout=sub.PIPE)            
      resultD = pigD.communicate(input=b"This is sample text.\n")
      exe_resultD = str(resultD[0],'utf-8')
      pigD.kill()
      #print("exe",exe_resultD)
      #####################################################
      df4 = getCsvFromCppResults(exe_resultD, 'DENSITYSLICE')
      df5 = getCsvFromCppResults(exe_resultD, 'RADIANTSLICE')
      df6 = getCsvFromCppResults(exe_resultD, 'LAPLACIANSLICE')      
      return [df1,df2,df3,df4,df5,df6]
    #except:
      #print("results from exe=",result)
      #return []

    

