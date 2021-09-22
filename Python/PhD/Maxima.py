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
import sys
import Config as cfg

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
  haveED = False
  havePDB = False
  import os
  directory = '/d/projects/u/ab002/Thesis/PhD/Data/'
  allFiles = True
  #Files from the PDBE	
  origPdb = directory + 'Pdb/pdb' + pdbCode + '.ent'
  ccp4File = directory + 'Ccp4/' + pdbCode + '.ccp4'
  ccp4Diff = directory + 'Ccp4/' + pdbCode + '_diff.ccp4'

  if pdbCode[:5] == "user_":
    origPdb = cfg.UserDataPdbDir + 'pdb' + pdbCode + '.ent'
    ccp4File = cfg.UserDataCcp4Dir + pdbCode + '.ccp4'
    ccp4Diff = cfg.UserDataCcp4Dir + pdbCode + '.ccp4' # no diff file

  if os.path.isfile(origPdb):
    havePDB = True
  else:
    try:
      getFile(origPdb,'https://www.ebi.ac.uk/pdbe/entry-files/download/pdb' + pdbCode + '.ent')
      havePDB = True
    except:
      havePDB = False

  if os.path.isfile(ccp4File):
    haveED = True
  else:
    try:
      getFile(ccp4File,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode + '.ccp4')
      getFile(ccp4Diff,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode +'_diff.ccp4')
      haveED = True
    except:
      haveED = False
      
  return havePDB,haveED

def runCppModule(pdb,interpNum,Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7):        
    #try:
    df1a,df1b,df1c,df3,df4,df5,df6 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    if True:
      ### CALL PEAKS ######################################
      if D1 or D2 or D3 or D4:
        commandlinePeaks = "PEAKS|" + pdb + "|" + str(interpNum) + "|" + str(Fos) + "|"+ str(Fcs) + "|"
        #print('...called Leucippus with params:' + commandlinePeaks + ' ...')                      
        #------------------------------------------------
        pigP =  sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlinePeaks], stdout=sub.PIPE)
        resultP = pigP.communicate(input=b"This is sample text.\n")
        exe_resultP = str(resultP[0],'utf-8')
        pigP.kill()
        #------------------------------------------------
        dfInputs = getCsvFromCppResults(exe_resultP, 'USERINPUTS')      
        df1a = getCsvFromCppResults(exe_resultP, 'ALLPEAKS')
        if len(df1a) == 0:
          print("results from exe=",resultP)
          return []      
        df1b = getCsvFromCppResults(exe_resultP, 'ATOMPEAKS')
        df1c = getCsvFromCppResults(exe_resultP, 'CHIMERAPEAKS')
      
      ### CALL ATOMS ######################################
      if D5 or D6:
        commandlineAtoms = "ATOMS|" + pdb + "|" + str(interpNum) + "|"+ str(Fos) + "|"+ str(Fcs) + "|"
        #print('...called Leucippus with params:' + commandlineAtoms + ' ...')        
        #------------------------------------------------
        pigA = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlineAtoms], stdout=sub.PIPE)            
        resultA = pigA.communicate(input=b"This is sample text.\n")
        exe_resultA = str(resultA[0],'utf-8')
        pigA.kill()      
        #------------------------------------------------
        df3 = getCsvFromCppResults(exe_resultA, 'ATOMDENSITY')

      ### CALL SLICES #######################################
      if D7:
        commandlineSlices = "SLICES|" + pdb + "|" + str(interpNum) + "|" + str(Fos) + "|"+ str(Fcs) + "|"        
        commandlineSlices += str(cX) + "-" + str(cY) + "-" + str(cZ) + "|"
        commandlineSlices += str(lX) + "-" + str(lY) + "-" + str(lZ) + "|"
        commandlineSlices += str(pX) + "-" + str(pY) + "-" + str(pZ) + "|"
        commandlineSlices += str(width) + "-" + str(gran)
        #print('...called Leucippus with params:' + commandlineSlices + ' ...')        
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

      return [[df1a,df1b,df1c],[df3],[df4,df5,df6]]
    #except:
      #print("results from exe=",result)
      #return []


def runCppModuleSyntheticDensity(atoms,model,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran):        
    #try:
    df1a,df1b,df1c,df1d = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    if True:
      ### CALL Synthetic Density ######################################              
      commandlineSnth = "SYNTHETIC|" + atoms + "|" + model + "|2|-1|"        
      commandlineSnth += str(cX) + "-" + str(cY) + "-" + str(cZ) + "|"
      commandlineSnth += str(lX) + "-" + str(lY) + "-" + str(lZ) + "|"
      commandlineSnth += str(pX) + "-" + str(pY) + "-" + str(pZ) + "|"
      commandlineSnth += str(width) + "-" + str(gran)          
      #print('...called Leucippus with params:' + commandlineSnth + ' ...')
      
      
      #------------------------------------------------
      pigS = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandlineSnth], stdout=sub.PIPE)            
      resultS = pigS.communicate(input=b"This is sample text.\n")
      exe_resultS = str(resultS[0],'utf-8')
      pigS.kill()      
      #------------------------------------------------            
      #dfI = getCsvFromCppResults(exe_resultS, 'USERINPUTS')
      #print(dfI)
      dfI = getCsvFromCppResults(exe_resultS, 'ATOMDATA')
      #print(dfI)

      df1a = getCsvFromCppResults(exe_resultS, 'DENSITYSLICE')
      df1b = getCsvFromCppResults(exe_resultS, 'RADIANTSLICE')
      df1c = getCsvFromCppResults(exe_resultS, 'LAPLACIANSLICE')
      df1d = getCsvFromCppResults(exe_resultS, 'POSITIONSLICE')
      #df1d = getCsvFromCppResults(exe_resultS, 'SYNTHMATRIX')      

      return [df1a,df1b,df1c,df1d]
    #except:
      #print("results from exe=",result)
      #return []

    

