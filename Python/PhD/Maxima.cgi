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
# Data return choices
D1, D2, D3, D4, D5, D6, D7 = False,False,False,False,False,False,False
width = 5
gran = 0.1

form = cgi.FieldStorage()

if 'dataInput' in form:
  pdb = str(form["dataInput"].value)
if 'format' in form:  
  asCSV = "asCsv"== str(form["format"].value)
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
  
access = pwb.userSuccess(username,password)
html = pwb.getHeader()
html += pwb.getBodyA(pdb,asCSV,username,password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7)
if access:
  done = Maxima.doWeHaveAllFiles(pdb)
  data = Maxima.runCppModule(pdb,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7)
  html += pwb.getBodyB(pdb,data,asCSV,D1,D2,D3,D4,D5,D6,D7)
  html += pwb.getBodyC(pdb,data,width,gran,D1,D2,D3,D4,D5,D6,D7)
  #html += pwb.getBodyD(pdb,data,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ)
else:
  html += "<h2>!!No access!! Enter a valid email address.</h2>"

html += pwb.getFooter()

print(html)

#************************************************************************************************
