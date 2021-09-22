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
import Config as cfg
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


#FILE UPLOAD CODE
try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()


userCode = ''
UserCcp4 = False
UserPdb = False

if 'userCode' in form:
  userCode = form["userCode"].value
  userCode = userCode.lower()

if 'fileCcp4' in form:
  fileitem = form["fileCcp4"].value    
  if len(fileitem) > 20:
      open(cfg.UserDataCcp4Dir + 'user_' + userCode + '.ccp4', 'wb').write(fileitem)
      UserCcp4 = True

if 'filePdb' in form:
  fileitem = form["filePdb"].value
  if len(fileitem) > 20:
      open(cfg.UserDataPdbDir + 'pdbuser_' + userCode + '.ent', 'wb').write(fileitem)
      UserPdb = True


#we are creating 2 HTML files, the cgi script and the html document
userstring = ""
cgistring = ""

if 'email' in form:  
  username = str(form["email"].value)
if 'password' in form:  
  password = str(form["password"].value)

access = pwb.userSuccess(username,password)
html = pwb.getHeader()
cgistring += html

print(cgistring)
sys.stdout.flush() # update the user interface
cgistring = ""


cgistring += pwb.getBodyUserUpload(userCode,username,password)
if access:
  havepdb, haveed = Maxima.doWeHaveAllFiles("user_" + userCode)
  
  if havepdb and haveed:
            
      cgistring += '<hr/><h3>File Upload Results</h3>'
      cgistring += '<p>You may now use your uploaded file with the pseudo-pdbcode <b>user_'
      cgistring += userCode + '</b> where a pdbcode is requested</p>'
      
    
              
  else:
    if not havepdb:
      cgistring += "<h2>!!! There is no pdb file uploaded for " + userCode + " !!!</h2>"
    if not haveed:
      cgistring += "<h2>!!! There is no electron density uploaded for " + userCode + " !!!</h2>"
  
else:
  cgistring += "<h2>!!! No access !!! Enter a valid email address.</h2>"


#print out the options to the cgi

cgistring += pwb.getFooter()

print(cgistring)

#************************************************************************************************
