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
  #import urllib.request  
  #urllib.request.urlretrieve(url,filename)
  import requests #https://stackoverflow.com/questions/32763720/timeout-a-file-download-with-python-urllib
  request = requests.get(url, timeout=100, stream=True)  
  with open(filename, 'wb') as fh:    # Open the output file and make sure we write in binary mode
    count = 0
    for chunk in request.iter_content(1024 * 1024*10): # Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
        fh.write(chunk)
        print(count,end=',')
        count +=1
        sys.stdout.flush()
  print('Downloaded')
        
  

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
  
def doWeHaveAllFiles(pdbCode,debug=False):
  haveED = False
  havePDB = False
  import os
  allFiles = True
  #Files from the PDBE
  directory = '/d/projects/u/ab002/Thesis/PhD/Data/'
  origPdb = cfg.PdbDir + 'pdb' + pdbCode + '.ent'
  ccp4File = cfg.Ccp4Dir + pdbCode + '.ccp4'
  ccp4Diff = cfg.Ccp4Dir + pdbCode + '_diff.ccp4'
  isXray = True
  ccp4Num = '0'
  pdbOnly = pdbCode

  if pdbCode[:5] == "user_":
    origPdb = cfg.UserDataPdbDir + 'pdb' + pdbCode + '.ent'
    ccp4File = cfg.UserDataCcp4Dir + pdbCode + '.ccp4'
    ccp4Diff = cfg.UserDataCcp4Dir + pdbCode + '.ccp4' # no diff file
  elif pdbCode[:4] == 'emdb':
    # Find the number and the pdb code from the format emdb_12345_1abc
    inps = pdbCode.split('_')
    pdbNewCode = 'emdb_' + inps[2]    
    ccp4NewCode = 'emdb_' + inps[1]
    origPdb = cfg.EmdbPdbDir + 'pdb' + pdbNewCode + '.ent'
    pdbOnly = inps[2]      
    ccp4FileZip = cfg.EmdbCcp4Dir + ccp4NewCode + '.map.gz'
    ccp4File = cfg.EmdbCcp4Dir + ccp4NewCode + '.ccp4'    
    isXray = False
    ccp4Num = inps[1]
  
  if os.path.isfile(origPdb):
    havePDB = True
  else:
    try:      
      getFile(origPdb,'https://www.ebi.ac.uk/pdbe/entry-files/download/pdb' + pdbOnly + '.ent')      
      havePDB = True
    except:
      havePDB = False

  if os.path.isfile(ccp4File):
    haveED = True
  else:
    try:
      if isXray:
        getFile(ccp4File,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode + '.ccp4')
        getFile(ccp4Diff,'https://www.ebi.ac.uk/pdbe/coordinates/files/' + pdbCode +'_diff.ccp4')
      else:
        emdbPath = 'https://ftp.ebi.ac.uk/pub/databases/emdb/structures/EMD-' + ccp4Num + '/map/emd_' + ccp4Num + '.map.gz'        
        if not os.path.isfile(ccp4FileZip):
          print('This file needs to be downloaded: ', emdbPath)
          print('\n')
          print('EMDB map files can be large, contact us if there are any problems with this file\n')
          getFile(ccp4FileZip,emdbPath)

        import gzip
        import shutil
        #https://www.codegrepper.com/code-examples/python/how+to+extract+gz+file+python
        # now we need to unzip it
        print('Unzipping...')
        sys.stdout.flush()
        with gzip.open(ccp4FileZip,'rb') as f_in:
          with open(ccp4File,'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)

        print('...unzipped')
        sys.stdout.flush()
        import os
        os.remove(ccp4FileZip)
        
      haveED = True        
    except:
      haveED = False
      
  return havePDB,haveED

def runCppModule(pdb,interpNum,Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7,D8,D9,debug=False):
    #try:
    import Config as cfg
    df1a,df1b,df1c = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    df2a, df2b, df2c = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df4, df5, df6,df7 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    exePath =cfg.ExePath

    if True:
      ### CALL PEAKS ######################################
      if D1 or D2 or D3 or D4:        
        commandlinePeaks = "PEAKS|" + pdb + "|" + str(interpNum) + "|" + str(Fos) + "|"+ str(Fcs) + "|"
        #print('...called Leucippus with params:' + commandlinePeaks + ' ...')
        #sys.stdout.flush() # update the user interface
        #------------------------------------------------
        pigP =  sub.Popen([exePath, commandlinePeaks], stdout=sub.PIPE)
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
        commandlineAtoms = "ATOMSDENSITY|" + pdb + "|" + str(interpNum) + "|"+ str(Fos) + "|"+ str(Fcs) + "|"
        #print('...called Leucippus with params:' + commandlineAtoms + ' ...')        
        #------------------------------------------------
        pigA = sub.Popen([exePath, commandlineAtoms], stdout=sub.PIPE)
        resultA = pigA.communicate(input=b"This is sample text.\n")
        exe_resultA = str(resultA[0],'utf-8')
        pigA.kill()      
        #------------------------------------------------
        df2a = getCsvFromCppResults(exe_resultA, 'ATOMDENSITY')
                
      ### CALL ATOMS ######################################
      if D7 or D8:
        commandlineAtomsAdj = "ATOMSADJUSTED|" + pdb + "|" + str(interpNum) + "|"+ str(Fos) + "|"+ str(Fcs) + "|"
        #print('...called Leucippus with params:' + commandlineAtoms + ' ...')        
        #------------------------------------------------
        pigAa = sub.Popen([exePath, commandlineAtomsAdj], stdout=sub.PIPE)
        resultAa = pigAa.communicate(input=b"This is sample text.\n")
        exe_resultAa = str(resultAa[0],'utf-8')
        pigAa.kill()      
        #------------------------------------------------        
        df2b = getCsvFromCppResults(exe_resultAa, 'DENSITYADJUSTED')
        df2c = getCsvFromCppResults(exe_resultAa, 'LAPLACIANADJUSTED')
        
          
        
      ### CALL SLICES #######################################
      if D9:
        commandlineSlices = "SLICES|" + pdb + "|" + str(interpNum) + "|" + str(Fos) + "|"+ str(Fcs) + "|"        
        commandlineSlices += str(cX) + "_" + str(cY) + "_" + str(cZ) + "|"
        commandlineSlices += str(lX) + "_" + str(lY) + "_" + str(lZ) + "|"
        commandlineSlices += str(pX) + "_" + str(pY) + "_" + str(pZ) + "|"
        commandlineSlices += str(width) + "_" + str(gran)

        print('...called Leucippus with params:' + commandlineSlices + ' ...')        
        #------------------------------------------------
        pigS = sub.Popen([exePath, commandlineSlices], stdout=sub.PIPE)
        resultS = pigS.communicate(input=b"This is sample text.\n")
        exe_resultS = str(resultS[0],'utf-8')
        pigS.kill()      
        #------------------------------------------------
        #dfI = getCsvFromCppResults(exe_resultS, 'USERINPUTS')
        #print(dfI)
        df4 = getCsvFromCppResults(exe_resultS, 'DENSITYSLICE')
        df5 = getCsvFromCppResults(exe_resultS, 'RADIANTSLICE')
        df6 = getCsvFromCppResults(exe_resultS, 'LAPLACIANSLICE')
        df7 = getCsvFromCppResults(exe_resultS, 'POSITIONSLICE')

      return [[df1a,df1b,df1c],[df2a,df2b,df2c],[df4,df5,df6,df7]]
    #except:
      #print("results from exe=",result)
      #return []

def runCppModuleText(pdb):
    commandline = "TEXTCOUT|" + pdb + "|5|-2|1|"
    df1 = pd.DataFrame()
    #print(commandline)
    pig = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", commandline], stdout=sub.PIPE)            
    try:
      result = pig.communicate(input=b"This is sample text.\n")
      exe_result = str(result[0],'utf-8')
    except:
      pig.kill()
      result = pig.communicate(input=b"This is sample text.\n")
      exe_result = str(result[0],'utf-8')
    #print(exe_result)    
    df1 = getCsvFromCppResults(exe_result, 'RAWTEXT')
    pig.kill()
    #print(df1)
    return [df1]

def runCppModuleSyntheticDensity(atoms,model,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran):        
    #try:
    df1a,df1b,df1c,df1d = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    if True:
      ### CALL Synthetic Density ######################################              
      commandlineSnth = "SYNTHETIC|" + atoms + "|" + model + "|2|-1|"        
      commandlineSnth += str(cX) + "_" + str(cY) + "_" + str(cZ) + "|"
      commandlineSnth += str(lX) + "_" + str(lY) + "_" + str(lZ) + "|"
      commandlineSnth += str(pX) + "_" + str(pY) + "_" + str(pZ) + "|"
      commandlineSnth += str(width) + "_" + str(gran)          
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


def runCppModuleSamples(pdb):
  # try:
  df1a, df1b = pd.DataFrame(), pd.DataFrame()
  if True:
    ### CALL Synthetic Density ######################################
    commandlineSnth = "SAMPLES|" + pdb + "|5|2|-1|"
    print('...called Leucippus with params:' + commandlineSnth + ' ...', cfg.ExePath)

    # ------------------------------------------------
    pigS = sub.Popen([cfg.ExePath, commandlineSnth],stdout=sub.PIPE)
    resultS = pigS.communicate(input=b"This is sample text.\n")
    exe_resultS = str(resultS[0], 'utf-8')
    pigS.kill()
    # ------------------------------------------------
    df1a = getCsvFromCppResults(exe_resultS, 'DENSITYADJUSTED')
    df1b = getCsvFromCppResults(exe_resultS, 'LAPLACIANADJUSTED')

    return [pd.DataFrame(),df1a, df1b] #to be consistent, should be changes TODO




