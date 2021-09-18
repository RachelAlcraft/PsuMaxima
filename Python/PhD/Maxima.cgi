#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      26/08/2021
Function:  A CGI file to take text and run an external C++ file
Description: 
============

"""

#************************************************************************************************

import cgi
import sys
import Maxima
import PhdWebBuilder as pwb
import time

### HELPER FUNCTIONS ####################################################
def getTimeDiff(start,end):
    time_diff = end - start
    timestring = str(int(time_diff/60)) + "m " + str(int(time_diff%60)) + "s"
    return timestring
############################################################################

# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")


#we are creating 2 HTML files, the cgi script and the html document
userstring = ""
cgistring = ""

pdb = '1ejg'
interpNum = 2
asCSV = True
cX,cY,cZ = 0,0,0
lX,lY,lZ = 0,0,0
pX,pY,pZ = 0,0,0
username = ""
password = ""
# Data return choices
D1, D2, D3, D4, D5, D6, D7 = False,False,False,False,False,False,False
width = 5
gran = 0.1
interpMethod = 'spline'

form = cgi.FieldStorage()

if 'dataInput' in form:
  pdb = str(form["dataInput"].value)
if 'interpNum' in form:
  interpNum = int(form["interpNum"].value)
if 'format' in form:  
  asCSV = "asCsv"== str(form["format"].value)
if 'interpMethod' in form:  
  interpMethod = str(form["interpMethod"].value)
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

# RESULTS
if form.getvalue('Data1'):
   D1=True
if form.getvalue('Data2'):
   D2=True
if form.getvalue('Data3'):
   D3=True
if form.getvalue('Data4'):
   D4=True
if form.getvalue('Data5'):
   D5=True
if form.getvalue('Data6'):
   D6=True
if form.getvalue('Data7'):
   D7=True
  
if interpMethod == "spline":
  interpNum = 5
else:
  interpNum = 0

peaksTime = 50#10 + (interpNum*interpNum)
if interpMethod == "nearest":
  peaksTime = 15 


access = pwb.userSuccess(username,password)
html = pwb.getHeader()
userstring += html
cgistring += html

print(cgistring)
sys.stdout.flush() # update the user interface
cgistring = ""


userstring += pwb.getBodyA(pdb,interpNum,asCSV,username,password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,interpMethod,D1,D2,D3,D4,D5,D6,D7)
if access:
  havepdb, haveed = Maxima.doWeHaveAllFiles(pdb)
  userstring += pwb.getBodyRun0(pdb)

  #print('Access granted')
  #sys.stdout.flush() # update the user interface

  totalRuns = 0
  if D1 or D2 or D3:
    totalRuns += 1
  if D4 or D5 or D6:
    totalRuns += 1
  if D7:
    totalRuns += 1

  runNo = 0
  

  if havepdb and haveed:
    # Peaks run
    if D1 or D2 or D3 or D3:
      runNo += 1
      print('<p>' + str(runNo) + '/' + str(totalRuns) + ' Calculating peaks...(approx ' + str(peaksTime) + ' seconds)...')      
      sys.stdout.flush() # update the user interface      
      start = time.time()
      data = Maxima.runCppModule(pdb,interpNum,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,False,False,False,False)
      userstring += pwb.getBodyRun1(pdb,data[0],asCSV,D1,D2,D3,D4)
      end = time.time()
      ts = getTimeDiff(start,end)
      print('completed in')
      print(ts)
      print(' <p>')
      sys.stdout.flush() # update the user interface
      
      
    if D5 or D6:
      runNo += 1
      print('<p>' + str(runNo) + '/' + str(totalRuns) + ' Inspecting atoms...(approx 45 seconds)...')      
      sys.stdout.flush() # update the user interface
      start = time.time()
      data = Maxima.runCppModule(pdb,interpNum,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,False,False,False,D4,D5,D6,False)
      userstring += pwb.getBodyRun2(pdb,data[1],D5,D6)
      end = time.time()
      ts = getTimeDiff(start,end)
      print('completed in')
      print(ts)
      print(' <p>')
      sys.stdout.flush() # update the user interface
      html = ""

    if D7:
      runNo += 1
      print('<p>' + str(runNo) + '/' + str(totalRuns) + ' Visualising density...(approx 5 seconds)...')      
      sys.stdout.flush() # update the user interface
      start = time.time()
      data = Maxima.runCppModule(pdb,interpNum,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,False,False,False,False,False,False,D7)
      userstring += pwb.getBodyRun3(pdb,data[2],width,gran,D7)
      end = time.time()
      ts = getTimeDiff(start,end)
      print('completed in')
      print(ts)
      print(' <p>')
      sys.stdout.flush() # update the user interface
        
      
    #we now create the users own html page
    userstring += pwb.getFooter()
    results = pwb.userOwnWebPage(username,userstring)

    #and inform the cgi script of the results
    print(results)
    sys.stdout.flush() # update the user interface
    
    
  else:
    if not havepdb:
      cgistring += "<h2>!!! There is no pdb file named " + pdb + " !!!</h2>"
    if not haveed:
      cgistring += "<h2>!!! There is no electron density for " + pdb + " !!!</h2>"
  
else:
  cgistring += "<h2>!!! No access !!! Enter a valid email address.</h2>"


#print out the options to the cgi

cgistring += pwb.getBodyA(pdb,interpNum,asCSV,username,password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,interpMethod,D1,D2,D3,D4,D5,D6,D7)
cgistring += pwb.getFooter()


print(cgistring)

#************************************************************************************************
