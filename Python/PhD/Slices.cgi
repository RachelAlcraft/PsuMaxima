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

pdbCode = ''
interpMethod = ''
cX,cY,cZ = 0,0,0
lX,lY,lZ = 0,0,0
pX,pY,pZ = 0,0,0
username = ""
password = ""
Fos = 2
Fcs = -1
# Data return choices

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


access = pwb.userSuccess(username,password)
html = pwb.getHeader()
userstring += html
cgistring += html

print(cgistring)
sys.stdout.flush() # update the user interface
cgistring = ""


userstring += pwb.getBodySlices(pdbCode, username, password,interpMethod, Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran)
if access:  
  print('<p>' + str(1) + '/' + str(1) + ' Calculating local map slices...(approx ' + str(6) + ' seconds)...')  
  sys.stdout.flush() # update the user interface      
  start = time.time()
  data = Maxima.runCppModule(pdbCode,interpNum,Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,False,False,False,False,False,False,False,False,True)
  userstring += pwb.getBodyRun3(pdbCode,data[2],width,gran,True)
  end = time.time()
  ts = getTimeDiff(start,end)
  print('completed in')
  print(ts)
  print(' </p>')
  sys.stdout.flush() # update the user interface
          
  #we now create the users own html page
  userstring += pwb.getFooter()
  results = pwb.userOwnWebPage(username,userstring)

  #and inform the cgi script of the results
  print(results)
  sys.stdout.flush() # update the user interface
    
        
else:
  cgistring += "<h2>!!! No access !!! Enter a valid email address.</h2>"


#print out the options to the cgi

cgistring += pwb.getBodySlices(pdbCode, username, password,interpMethod,Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran)
cgistring += pwb.getFooter()


print(cgistring)

#************************************************************************************************
