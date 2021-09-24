#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      23/09/2021
Function:  STRAIGHT CALLS TO THE EXE FOR TESTING
Description:
============

"""

# ************************************************************************************************

import sys
import Maxima
import PhdWebBuilder as pwb
import time

### HELPER FUNCTIONS ####################################################
def getTimeDiff(start, end):
    time_diff = end - start
    timestring = str(int(time_diff / 60)) + "m " + str(int(time_diff % 60)) + "s"
    return timestring


############################################################################
userstring = ""
pdb = '1ejg'
interpNum = 2
asCSV = True
cX, cY, cZ = 0, 0, 0
lX, lY, lZ = 0, 0, 0
pX, pY, pZ = 0, 0, 0
username = "RachelTest"
password = ""
# Data return choices
# PEAKS
D1, D2, D3, D4 = False, False, False, False #vis projection, pseudo file, html grid, unit cell
# ATOMS
D5,D6,D7,D8 = True,True,True,True #atoms projection, atomno projection, density adjusted, laplacian adjusted
# SLICES
D9 =  False

width = 5
gran = 0.1
interpMethod = 'spline'
Fos = 2
Fcs = -1


#####################################################
if interpMethod == "spline":
    interpNum = 5
else:
    interpNum = 0
peaksTime = 50  # 10 + (interpNum*interpNum)
if interpMethod == "nearest":
    peaksTime = 15

html = pwb.getHeader()
userstring += html
sys.stdout.flush()  # update the user interface

if True:
    havepdb, haveed = Maxima.doWeHaveAllFiles(pdb, True)
    userstring += pwb.getBodyRun0(pdb)

    if havepdb and haveed:
        # Peaks run
        if D1 or D2 or D3 or D4:
            start = time.time()
            print('Starting exe, estimate 50 sec...')
            data = Maxima.runCppModule(pdb, interpNum, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ, width, gran, D1,
                                       D2, D3, D4, False, False, False,False,False,debug=True)
            userstring += pwb.getBodyRun1(pdb, data[0], asCSV, D1, D2, D3, D4,debug=True)
            end = time.time()
            ts = getTimeDiff(start, end)
            print('completed in',ts)
        if D5 or D6 or D7 or D8:
            start = time.time()
            print('Starting exe, estimate 40 sec...')
            data = Maxima.runCppModule(pdb, interpNum, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ, width, gran, False, False, False,False,D5, D6,D7,D8,False, debug=True)
            userstring += pwb.getBodyRun2(pdb, data[1], D5, D6,D7,D8,debug=True)
            end = time.time()
            ts = getTimeDiff(start, end)
            print('completed in',ts)
            html = ""
        if D9:
            print('Starting exe, estimate 20 sec...')
            start = time.time()
            data = Maxima.runCppModule(pdb, interpNum, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ, width, gran, False,
                                       False, False, False, False, False, False,False,D9,debug=True)
            userstring += pwb.getBodyRun3(pdb, data[2], width, gran, D7)
            end = time.time()
            ts = getTimeDiff(start, end)
            print('completed in',ts)
        # we now create the users own html page
        userstring += pwb.getFooter()
        results = pwb.userOwnWebPage(username, userstring,True)

        # and inform the cgi script of the results
        print(results)
        sys.stdout.flush()  # update the user interface


    else:
        if not havepdb:
            print('!!! There is no pdb file named ',pdb,' !!!')
        if not haveed:
            print('!!! There is no electron density file for ',pdb,' !!!')

else:
    print('!!! No access !!! Enter a valid email address')

# ************************************************************************************************
