#!/l_mnt/python/envs/teaching/bin/python3 
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
import Geometry.Geometry as geo
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

username = ''
password = ''

pdbCodeA = ''
pdbCodeB = ''
GeoA = ''
GeoB = ''
GeoC = ''

form = cgi.FieldStorage()
if 'PdbA' in form:
  pdbCodeA = str(form["PdbA"].value)
if 'PdbB' in form:
  pdbCodeB = str(form["PdbB"].value)
if 'email' in form:  
  username = str(form["email"].value)
if 'password' in form:  
  password = str(form["password"].value)
if 'GeoHueA' in form:  
  GeoA = str(form["GeoHueA"].value)
if 'GeoHueB' in form:  
  GeoB = str(form["GeoHueB"].value)
if 'GeoHueA' in form:  
  GeoC = str(form["GeoHueC"].value)
  

pathA = '/d/user6/ab002/Desktop/Link to Thesis/PhD/Data/Pdb/'
pathB = '/d/user6/ab002/Desktop/Link to Thesis/PhD/Data/Pdb/'
if pdbCodeA[:4] == 'user':
    pathA = '/d/user6/ab002/Desktop/Link to Thesis/PhD/Data/UserPdb/'
if pdbCodeB[:4] == 'user':
    pathB = '/d/user6/ab002/Desktop/Link to Thesis/PhD/Data/UserPdb/'

access = pwb.userSuccess(username,password)
html = pwb.getHeader(Geometry=True)
userstring += html
cgistring += html

print(cgistring)
sys.stdout.flush() # update the user interface
cgistring = ""


userstring += pwb.getBodyGeometry(pdbCodeA, pdbCodeB, username, password,GeoA, GeoB, GeoC)
success = False
if access:  
  print('<p>' + str(1) + '/' + str(1) + ' Calculating pdb geoemtry..(approx ' + str(8) + ' seconds)...')  
  sys.stdout.flush() # update the user interface      
  start = time.time()

  try:
      userstring += geo.innerStringTwoPdbCompare(pdbCodeA,pdbCodeB,pathA,pathB,GeoA,GeoB,GeoC)
      end = time.time()
      ts = getTimeDiff(start,end)
      print('completed in')
      print(ts)
      print(' </p>')
      sys.stdout.flush() # update the user interface
      Success = True
      #we now create the users own html page
      userstring += pwb.getFooter()
      results = pwb.userOwnWebPage(username,userstring)

      #and inform the cgi script of the results
      print(results)
      sys.stdout.flush() # update the user interface
  
  except:
      cgistring += "<h2>!!! Something has gone wrong, check your inputs !!! </h2>"
            
    
  
    
        
else:
  cgistring += "<h2>!!! No access !!! Enter a valid email address.</h2>"


#print out the options to the cgi

cgistring += pwb.getBodyGeometry(pdbCodeA, pdbCodeB, username, password,GeoA, GeoB, GeoC)
cgistring += pwb.getFooter()


print(cgistring)

#************************************************************************************************

