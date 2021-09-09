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
import Maxima
import PhdWebBuilder as pwb


# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")

pdb = '1ejg'
asCSV = True
cX,cY,cZ = 0,0,0
lX,lY,lZ = 0,0,0
pX,pY,pZ = 0,0,0
username = ""
password = ""

form = cgi.FieldStorage()
if 'dataInput' in form:
  pdb = str(form["dataInput"].value)
if 'format' in form:  
  asCSV = "asCsv"== str(form["format"].value)
if 'email' in form:  
  username = str(form["email"].value)
if 'password' in form:  
  password = str(form["password"].value)
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
  

access = pwb.userSuccess(username,password)
html = pwb.getHeader()
html += pwb.getBodyA(pdb,asCSV,username,password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ)
if access:
  done = Maxima.doWeHaveAllFiles(pdb)
  data = Maxima.runCppModule(pdb,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ)
  html += pwb.getBodyB(pdb,data,asCSV)
  html += pwb.getBodyC(pdb,data)
  #html += pwb.getBodyD(pdb,data,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ)
else:
  html += "<h2>!!No access!! Enter a valid email address.</h2>"

html += pwb.getFooter()

print(html)

#************************************************************************************************
