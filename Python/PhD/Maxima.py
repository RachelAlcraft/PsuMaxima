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


def doWeHaveAllFiles(pdbCode):
  done = True
  import os
  directory = '/d/projects/u/ab002/Thesis/PhD/Data/'
  allFiles = True
  #Files from the PDBE	
  origPdb = directory + 'Pdb' + pdbCode + '.ent'
  ccp4File = directory + 'Ccp4/' + pdbCode + '.ccp4'
  ccp4Diff = directory + 'Ccp4/' + pdbCode + '_diff.ccp4'

  if not os.path.isfile(origPdb):
    #print('getting pdb file from pdb</br>')    
    getFile(origPdb,'https://www.ebi.ac.uk/pdbe/entry-files/download/pdb3qr7.ent')

  if not os.path.isfile(ccp4File):
    #print('getting ccp4 files from pdb</br>')    
    getFile(ccp4File,'https://www.ebi.ac.uk/pdbe/coordinates/files/3qr7_diff.ccp4')
    getFile(ccp4Diff,'https://www.ebi.ac.uk/pdbe/coordinates/files/3qr7.ccp4')

  # Files to calculate
  adjPdb = directory + 'Adjusted/pdb' + pdbCode + '.ent'
  peaksFile = directory + 'Peaks/' + pdbCode + '_Maxa.csv'
  report =  directory + 'Report/MaximaDifferences_' + pdbCode + '.csv'

  return done

def runCppModule(dataText):
    ######### CHOOSE THE EXECUTABLE HERE #############
    #pig = sub.Popen(["F://Code//BioComputing2//BioComputing2//cgi-biocomp2//cpp//DummyCpp_Windows.exe", dataText], stdout=sub.PIPE)
    pig = sub.Popen(["/d/projects/u/ab002/Thesis/PhD/Github/PsuMaxima/Linux/build/PsuMaxima", dataText], stdout=sub.PIPE)
    #####################################################
    result = pig.communicate(input=b"This is sample text.\n")
    exe_result = str(result[0],'utf-8')
    exe_data = sio(exe_result)
    df = pd.read_csv(exe_data)
    #print(df)
    return df
    
#tst code for the dataframe
#exe_result = str(runCppModule("hi!"),'utf-8')    
#exe_data = sio(exe_result)
#df = pd.read_csv(exe_data)
