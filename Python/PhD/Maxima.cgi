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

pdb = '3qr7'
form = cgi.FieldStorage()
if 'dataInput' in form:
  pdb = str(form["dataInput"].value)
else:
  pdb = '3qr7';

done = Maxima.doWeHaveAllFiles(pdb)
data = Maxima.runCppModule(pdb)

html = pwb.getHeader()
html += pwb.getBodyA()
html += pwb.getBodyB(pdb,data)
html += pwb.getBodyC()
html += pwb.getBodyD(pdb,data)
html += pwb.getFooter()

print(html)

#************************************************************************************************
