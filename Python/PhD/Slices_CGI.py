#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      26/08/2021
Function:  A CGI file to take text and run an external C++ file
Description:
============

"""

# ************************************************************************************************

import cgi
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

# Useful debugging output
import cgitb

cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

# Print the HTML MIME-TYPE header
print("Content-Type: text/html\n")

# we are creating 2 HTML files, the cgi script and the html document
userstring = ""
cgistring = ""

interpMethod = 'spline'

pdbCode = '7a6a'
#smallest C:O
#cX, cY, cZ = 129.137,164.436,98.512 #C
#pX, pY, pZ = 128.451,164.563,99.464#O
#lX, lY, lZ = 130.435,164.683,98.532#N+1
#largetst C:0
#cX, cY, cZ = 146.596,86.651,140.976#C
#pX, pY, pZ = 145.472,86.173,140.666#O
#lX, lY, lZ = 146.919,87.885,140.731#N+1
#looking at OE2 bond with NA
#cX, cY, cZ = 147.915,87.284,145.793  #central OE2
#pX, pY, pZ = 148.495,86.177,145.470  #planar CD
#lX, lY, lZ = 146.996,89.166,146.996 #linear NA

#Adjusted position of largest C:O
#cX, cY, cZ = 146.626,86.681,140.946
#pX, pY, pZ = 145.299,86.277,140.653
#lX, lY, lZ = 146.841,87.836,140.653
#looking at OE2 bond with NA
#cX, cY, cZ = 148.161,86.606,145.547#r 134 OE2
#pX, pY, pZ = 148.687,85.985,145.662 #r 134 CD
#lX, lY, lZ = 147.100,89.062,147.100#HETATOM NA 202

#Looking at C and O and ...
na_adj = 147.100,89.062,147.100          #NA adj
n_adj = 148.948, 85.953,141.212          #N adj
ca_adj = 147.474,85.861,141.720          #CA adj
c_adj = 146.626,86.681,140.946           #C adj
o_adj = 145.299,86.277,140.653           #O adj
cb_adj = 147.533,86.442,143.253          #CB adj
cd_adj = 148.687,85.985,145.662          #CD adj
oe2_adj = 148.161,86.606,145.547         #OE2 adj
n1_adj = 146.841,87.836,140.653          #N+1 adj
soe2_adj = 145.548,87.999,149.554        #oe2 adj from S chain

cX, cY, cZ = c_adj
pX, pY, pZ = na_adj
lX, lY, lZ = oe2_adj





username = "testuser@slices"
password = ""
Fos = 2
Fcs = -1
# Data return choices
width=14
gran=0.05

form = cgi.FieldStorage()
if 'dataInput' in form:
    pdbCode = str(form["dataInput"].value)
if 'email' in form:
    username = str(form["email"].value)
if 'password' in form:
    password = str(form["password"].value)
# Points
if 'CX' in form:
    cX = str(form["CX"].value)
if 'CY' in form:
    cY = str(form["CY"].value)
if 'CZ' in form:
    cZ = str(form["CZ"].value)
if 'LX' in form:
    lX = str(form["LX"].value)
if 'LY' in form:
    lY = str(form["LY"].value)
if 'LZ' in form:
    lZ = str(form["LZ"].value)
if 'PX' in form:
    pX = str(form["PX"].value)
if 'PY' in form:
    pY = str(form["PY"].value)
if 'PZ' in form:
    pZ = str(form["PZ"].value)
# imgage settings
if 'Width' in form:
    width = str(form["Width"].value)
if 'Gran' in form:
    gran = str(form["Gran"].value)
if 'interpMethod' in form:
    interpMethod = str(form["interpMethod"].value)
if 'Fos' in form:
    Fos = form.getvalue('Fos')
if 'Fcs' in form:
    Fcs = form.getvalue('Fcs')

interpNum = 0
if interpMethod == "spline":
    interpNum = 5

access = True#pwb.userSuccess(username, password)
html = pwb.getHeader()
userstring += html
cgistring += html

print(cgistring)
sys.stdout.flush()  # update the user interface
cgistring = ""

userstring += pwb.getBodySlices(pdbCode, username, password, interpMethod, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ,
                                width, gran)
if access:
    havepdb, haveed = Maxima.doWeHaveAllFiles(pdbCode)
    if haveed and havepdb:
        if int(Fos) == 0 and int(Fcs) == 0:
            print('<p>' + str(1) + '/' + str(
                1) + ' Calculating IAM model from pdb coods for local map slices...(approx ' + str(60) + ' seconds)...')
        else:
            print('<p>' + str(1) + '/' + str(1) + ' Calculating local map slices...(approx ' + str(6) + ' seconds)...')
        sys.stdout.flush()  # update the user interface
        start = time.time()
        data = Maxima.runCppModule(pdbCode, interpNum, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ, width, gran, False,
                                   False, False, False, False, False, False, False, True)
        userstring += pwb.getBodyRun3(pdbCode, data[2], width, gran, True)
        end = time.time()
        ts = getTimeDiff(start, end)
        print('completed in')
        print(ts)
        print(' </p>')
        sys.stdout.flush()  # update the user interface

        # we now create the users own html page
        userstring += pwb.getFooter()
        results = pwb.userOwnWebPage(username, userstring)

        # and inform the cgi script of the results
        print(results)
        sys.stdout.flush()  # update the user interface
    else:
        cgistring += "<h2>!!! No pdb or electron  density found.</h2>"


else:
    cgistring += "<h2>!!! No access !!! Enter a valid email address.</h2>"

# print out the options to the cgi

cgistring += pwb.getBodySlices(pdbCode, username, password, interpMethod, Fos, Fcs, cX, cY, cZ, lX, lY, lZ, pX, pY, pZ,
                               width, gran)
cgistring += pwb.getFooter()

print(cgistring)

# ************************************************************************************************
