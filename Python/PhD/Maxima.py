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

def runCppModule(pdb, cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7):        
    #try:
    df1,df2,df3,df4,df5,df6 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    if True:
      ### CALL PEAKS ######################################
      if D1 or D2 or D3 or D4:
        commandlinePeaks = "PEAKS|" + pdb + "|"
        #------------------------------------------------
        pigP =  sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlinePeaks], stdout=sub.PIPE)
        resultP = pigP.communicate(input=b"This is sample text.\n")
        exe_resultP = str(resultP[0],'utf-8')
        pigP.kill()
        #------------------------------------------------
        dfInputs = getCsvFromCppResults(exe_resultP, 'USERINPUTS')      
        df1 = getCsvFromCppResults(exe_resultP, 'ALLPEAKS')
        if len(df1) == 0:
          print("results from exe=",result)
          return []      
        df2 = getCsvFromCppResults(exe_resultP, 'ATOMPEAKS')
      
      ### CALL ATOMS ######################################
      if D5 or D6:
        commandlineAtoms = "ATOMS|" + pdb + "|"
        #------------------------------------------------
        pigA = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlineAtoms], stdout=sub.PIPE)            
        resultA = pigA.communicate(input=b"This is sample text.\n")
        exe_resultA = str(resultA[0],'utf-8')
        pigA.kill()      
        #------------------------------------------------
        df3 = getCsvFromCppResults(exe_resultA, 'ATOMDENSITY')

      ### CALL SLICES #######################################
      if D7:
        commandlineSlices = "SLICES|" + pdb + "|"
        #Baffling, 6jvv only fails if I add more into the command line
        commandlineSlices += str(cX) + "-" + str(cY) + "-" + str(cZ) + "|"
        commandlineSlices += str(lX) + "-" + str(lY) + "-" + str(lZ) + "|"
        commandlineSlices += str(pX) + "-" + str(pY) + "-" + str(pZ) + "|"
        commandlineSlices += str(width) + "-" + str(gran)
        #------------------------------------------------
        pigS = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlineSlices], stdout=sub.PIPE)            
        resultS = pigS.communicate(input=b"This is sample text.\n")
        exe_resultS = str(resultS[0],'utf-8')
        pigS.kill()      
        #------------------------------------------------
        #dfI = getCsvFromCppResults(exe_resultS, 'USERINPUTS')
        #print(dfI)
        df4 = getCsvFromCppResults(exe_resultS, 'DENSITYSLICE')
        df5 = getCsvFromCppResults(exe_resultS, 'RADIANTSLICE')
        df6 = getCsvFromCppResults(exe_resultS, 'LAPLACIANSLICE')      

      return [df1,df2,df3,df4,df5,df6]
    #except:
      #print("results from exe=",result)
      #return []

    

