
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os

def userSuccess(email,password):
    isok = True
    #Does the email address contaion an @ sign?
    on_at = email.split('@')
    if len(on_at) != 2:
        isok = False
    on_dot = email.split('.')
    if len(on_dot) <2:
        isok = False

    directory = '/d/projects/u/ab002/Thesis/PhD/Data/Users/'
    filename = email
    if email != "rachelalcraft@gmail.com": #no point in me logging my 1000s of accesses!
        if not isok:
            filename += '_FAILED'
        
        from datetime import datetime
        dateTimeObj = datetime.now()
        dateObj = dateTimeObj.date()
        timestampStr = dateTimeObj.strftime("_%d_%b_%Y_%H_%M_%S_%f")
        filename += timestampStr + ".txt"
        f = open(directory+filename, "w")
        f.write("")
        f.close()
    
    return isok

def userOwnWebPage(email,string):
    isok = True
    #Does the email address contaion an @ sign?
    on_at = email.split('@')
    pageName = email#on_at[0] + "_" + on_at[1]

    directory = '/d/user6/ab002/WWW/Users/'
    filename = directory + pageName + ".html"
            
    f = open(filename, "w")
    f.write(string)
    f.close()

    res = ''
    res += '<hr/>'
    res += '<h3>Results ready for ' + pageName + '</h3>'
    res += '<p><i>This is your private results page, further results will be copied here, it will not be stored on the server so save as needed</i><p>'
    
    pathname = 'https://student.cryst.bbk.ac.uk/~ab002/Users/' + pageName + '.html'
    res += '<div style="background-color:SpringGreen;">'
    res += '<p><b><br/>   Results: </b>'
    res += '<a class="change_link_color" href="' + pathname + '" title="Results" target="_self">Link to your results</a>\n'
    res += '<br/><br/></p></div>'
    
    return res

def getHeader():
    string = '<!DOCTYPE html>\n'
    string += '<html lang="en">\n'
    string += '<head>\n'
    string += '<title>Leucippus Results</title>\n'   
    string += '<link rel="icon" href="/../../../~ab002/img/atom.ico" type="image/x-icon">\n'         
    string += '<style>\n'
    string += 'body {text-align:left;background-color:LightSteelBlue;margin-left: 52px;}\n'
    string += 'img {width:85%;border:1px solid MistyRose; }\n'    
    string += 'table {table-layout:fixed; text-align: center; border: 0.5px solid MistyRose; background: LightSteelBlue; padding: 0px;display: block;table-layout:fixed;}\n'
    string += 'td {padding:2px;border:0.5px solid rgb(180, 180, 280,0.75);background-color:AliceBlue;}\n'     
    string += 'a:link{color:MistyRose;}\n'
    string += 'a:visited {color:MistyRose;}\n'
    string += 'a:hover {color:white;}\n'
    string += 'a.change_link_color:link{color: black;}'
    string += 'a.change_link_color:visited{color: DarkSlateBlue;}'
    string += 'a.change_link_color:hover{color: Navy;}'
    string += '</style></head>\n'

    # header includes a bit of body, where we have the header...
    string += '<body>\n'
    string += '<hr/>'
    string += '<h1>\n'
    string += '<div style="background-color:black;padding:10px">\n'
    string += '<font color="DC143C">Leu</font><font color="AliceBlue">cip</font><font color="DC143C">pus</font>\n'
    string += '<img style="width:25px;border:2px;" src="/../../../~ab002/img/atom.ico" alt="Leucippus Atom">\n'
    string += '<font color="AliceBlue">Atomic </font><font color="Crimson">Density </font><font color="AliceBlue">Explorer</font>\n'
    string += '</div>\n'
    string += '</h1>'
    string += '<p style="background-color:Crimson;margin:5px;padding:5px;color:AliceBlue;">'
    string += '<a href="/../../~ab002/Leucippus.html" title="Home" target="_self">PhD Home</a>'
    string += " ~  <a href='/../../~ab002/InputPeaks.html' title='Home' target='_self'>User Uploads</a>\n"
    string += ' ~  <a href="/../../~ab002/Peaks.html" title="Home" target="_self">Peaks Explorer</a>'
    string += " ~  <a href='/../../~ab002/Slices.html' title='Home' target='_self'>Local Maps</a>\n"
    string += " ~  <a href='/../../~ab002/Documentation.html' title='Docs' target='_self'>About</a>"    
    string += " ~ <a href='https://www.bbk.ac.uk/departments/biology/' title='Birkbeck' target='_blank'>Birkbeck Biology</a>"
    string += '</p>'
    
    return string

def getBodyUserUpload(userCode, username, password):
    string = '<hr/>\n'
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Leu</font>cip<font color="DC143C">pus</font> - Atomic <font color="DC143C">Density</font> Explorer</h3>\n'
    string += '</p>\n'
    string += '<hr/>\n'
    string += '<h3>User File Upload</h3>\n'
    string += '<p>You may upload a ccp4 format file of electron density, and a matching pdb file with atomic coordinates here. You will then be able to use those files in Leucippus with the code we return to you in place of a pdb code.<br/>\n'
    string += 'Note that we expect a matching electron densiity and pdb file, the atomic coordinates are sued for distance reports. If you do not have a pdb file you can enter a blank file.<br/>\n'
    string += 'Note also that the Fo and Fc num that are passed in for ccp4 files are not used for user files - we assume you have manipulated the file into your desired format alresdy (it saves you also uploading a diff file).<br/><br/>\n'
    string += '<b>Please be aware that we do not keep the data for any guaranteed length of time and thise files are available for you to access and use on our servers during your session.</b>\n'
    string += '</p>\n'
    
    string += '<hr/>\n'
    string += '<div>\n'
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Upload.cgi" enctype="multipart/form-data" >\n'
    string += "<b>~~ Application access credentials ~~</b><br/><i>You must enter a valid email address to access this software. Passwords will be forthcoming.</i><br/>Email address: <input type='text' name='email' value='" + username + "' /> Password: <input type='text' name='password' value='not used' /><hr/>\n"
    
    string += '<hr/>\n'
    string += 'Enter a 4 character code for your files: <input type="text" name="userCode" value="' + userCode + '"><br/><br/>\n'
    string += 'Ccp4 File (ccp4 extension): <input type="file" name="fileCcp4"><br/><br/>\n'
    string += 'Pdb File (ent extension): <input type="file" name="filePdb"><br/><br/>\n'
    string += '<input type="submit" value="Upload"></p>\n'
    string += '</form>\n'
    string += '</div>\n'
    return string

def getBodySlices(pdbCode, username, password,interpMethod, Fos,Fcs,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran):

    splinechecked = 'checked="checked"'
    nearestchecked = ''
    if interpMethod == "nearest":
        nearestchecked = 'checked="checked"'
        splinechecked = ''
        
    string = '<hr/>\n'
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Leu</font>cip<font color="DC143C">pus</font> - Atomic <font color="DC143C">Density</font> Explorer</h3>\n'
    string += '</p>\n'
    string += '<p>\n'
    string += 'This webpage interfaces with a C++ executable which calculates synthetic density for the given atoms. This tool is used to explore Gaussian Overlap and Density Drift.\n'
    string += '</p>\n'
    string += '<hr/>\n'
    string += '<div>\n'
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Slices.cgi" accept-charset="UTF-8">\n'
    string += '<b>~~ Application access credentials ~~</b><br/><i>You must enter a valid email address to access this software. Passwords will be forthcoming.</i>\n'
    string += "<br/>Email address: <input type='text' name='email' value='" + username + "' />"
    string += " Password: <input type='text' name='password' value='not used' />"
    string += '<hr/>'
    string += '<h3>Local Map Visualisation</h3>\n'
    string += 'Enter 4 digit pdb code: <input type="text" name="dataInput" value=' + pdbCode + ' />\n'    
    string += '<table><tr><td style="background-color:Crimson;color:AliceBlue"">~~ Model Paramaters parameters ~~</td><td style="background-color:Crimson;color:AliceBlue"">~~ 3-point coordinates for plane ~~</td></tr>\n'
    string += '<tr><td>\n'
    string += '<div style="text-align: left;">\n'
    string += '<p><b>Interpolation:</b><br/>'
    string += '<input type="radio" id="spline" name="interpMethod" value="spline" ' + splinechecked + '><label for="spline">B-Spline</label><br/>'
    string += '<input type="radio" id="nearest" name="interpMethod" value="nearest" ' + nearestchecked + '><label for="nearest">Nearest Neighbour</label><br/>'
    string += '</p>'
    string += '<p><b>Fo and Fc numbers:</b><br/>\n'
    string += 'The main ccp4 file contains 2Fo-Fc<br/>\n'
    string += 'The diff file contains Fo-Fc<br/>\n'
    string += 'No Fos: <input type="text" name="Fos" value="' + Fos + '" size="2"/><br/>\n'
    string += 'No Fcs: <input type="text" name="Fcs" value="' + Fcs + '" size="2"/><br/>\n'
    string += '</p>\n'
    string += '</div></td>\n'
    string += '<td>\n'
    string += '<div style="text-align: left;"><b>Enter three points to get a density contour slice from the electron density.</b></div>\n'
    string += '<table style="background-color:AliceBlue;text-align:left;"><tr><td>Central: X=<input size="4" type="text" name="CX" value=' + str(cX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="CY" value=' + str(cY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="CZ" value=' + str(cZ) + ' /></td></tr>\n'
    string += '<tr><td>Linear: X=<input size="4" type="text" name="LX" value=' + str(lX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="LY" value=' + str(lY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="LZ" value=' + str(lZ) + ' /></td></tr>\n'
    string += '<tr><td>Planar: X=<input size="4" type="text" name="PX" value=' + str(pX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="PY" value=' + str(pY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="PZ" value=' + str(pZ) + ' /></td></tr></table>\n'
    string += '<div style="text-align: left;padding:5px"><b>Settings for image size</b></div>\n'
    string += '<table style="background-color:AliceBlue">\n'
    string += '<tr>\n'
    string += '<td>Width(&#8491;)=<input size="4" type="text" name="Width" value=' + str(width) + ' /> Granularity(&#8491;)=<input size="4" type="text" name="Gran" value=' + str(gran) + ' /></td>\n'
    string += '</tr>\n'
    string += '</table>\n'
    string += '</td></tr></table>\n'
    string += '<br/><input type="Submit" value="Analyse Local Maps"/>\n'
    string += '</form>\n'
    string += '</div>\n'
          
    return string



def getBodyMenuSynth(username, password,atoms,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,model):

    iamchecked = 'checked="checked"'
    bemchecked = ''
    if model == "bem":
        bemchecked = 'checked="checked"'
        iamchecked = ''

    string = '<hr/>\n'
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Leu</font>cip<font color="DC143C">pus</font> - Atomic <font color="DC143C">Density</font> Explorer</h3>\n'
    string += '</p>\n'
    string += '<p>\n'
    string += 'This webpage interfaces with a C++ executable which calculates synthetic density for the given atoms. This tool is used to explore Gaussian Overlap and Density Drift.\n'
    string += '</p>\n'
    string += '<hr/>\n'
    string += '<div>\n'
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Synthetic.cgi" accept-charset="UTF-8">\n'
    string += '<b>~~ Application access credentials ~~</b><br/><i>You must enter a valid email address to access this software. Passwords will be forthcoming.</i>\n'
    string += "<br/>Email address: <input type='text' name='email' value='" + username + "' />"
    string += " Password: <input type='text' name='password' value='not used' />"
    string += '<hr/>'
    string += '<h3>Synthetic Density Analysis</h3>\n'
    string += '<p>\n'
    string += 'Each row is an atom with type, coordinates, residue number (for bond electrons), bfactor, occupancy, arc parameters (end positions and number of positions).</br>\n'
    string += 'Example atoms have been entered for you which you can edit, the end positions are blank as no motion is being modelled. The format is a csv file, with the header above the text area (start the line with @).</br></br>\n'
    string += '<b>@Type,X,Y,Z,ResNo,BFactor,Occupancy,StartX,StartY,StartZ,EndX,EndY,EndZ,Count</b></br> \n'
    string += '<textarea style="white-space:pre-wrap;" id="atoms" name="atoms" rows="5" cols="120">\n'
    string += atoms    
    string += '</textarea>\n'
    string += '<p>\n'
    string += '<table><tr><td style="background-color:Crimson;color:AliceBlue"">~~ Model Paramaters parameters ~~</td><td style="background-color:Crimson;color:AliceBlue"">~~ 3-point coordinates for plane ~~</td></tr>\n'
    string += '<tr><td>\n'
    string += '<div style="text-align: left;">\n'
    string += '<p>Model:<br/>\n'
    string += '<input type="radio" id="iam" name="model" value="iam" ' + iamchecked + '"><label for="iam">Independent Atom Model</label><br/>\n'
    string += '<input type="radio" id="bem" name="model" value="bem" ' + bemchecked + '"><label for="bem">Bond Electron Model</label><br/><br/><br/><br/>\n'
    string += '</p>\n'
    string += '</div></td>\n'
    string += '<td>\n'
    string += '<div style="text-align: left;"><b>Enter three points to get a density contour slice from the electron density.</b></div>\n'
    string += '<table style="background-color:AliceBlue;text-align:left;"><tr><td>Central: X=<input size="4" type="text" name="CX" value=' + str(cX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="CY" value=' + str(cY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="CZ" value=' + str(cZ) + ' /></td></tr>\n'
    string += '<tr><td>Linear: X=<input size="4" type="text" name="LX" value=' + str(lX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="LY" value=' + str(lY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="LZ" value=' + str(lZ) + ' /></td></tr>\n'
    string += '<tr><td>Planar: X=<input size="4" type="text" name="PX" value=' + str(pX) + ' />\n'
    string += 'Y=<input size="4" type="text" name="PY" value=' + str(pY) + ' />\n'
    string += 'Z=<input size="4" type="text" name="PZ" value=' + str(pZ) + ' /></td></tr></table>\n'
    string += '<div style="text-align: left;padding:5px"><b>Settings for image size</b></div>\n'
    string += '<table style="background-color:AliceBlue">\n'
    string += '<tr>\n'
    string += '<td>Width(&#8491;)=<input size="4" type="text" name="Width" value=' + str(width) + ' /> Granularity(&#8491;)=<input size="4" type="text" name="Gran" value=' + str(gran) + ' /></td>\n'
    string += '</tr>\n'
    string += '</table>\n'
    string += '</td></tr></table>\n'
    string += '<br/><input type="Submit" value="Analyse Synthetic Density"/>\n'
    string += '</form>\n'
    string += '</div>\n'
    return string

    


def getBodyA(pdb, interpNum, dataAsCsv, username, password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,interpMethod,Fos,Fcs,D1,D2,D3,D4,D5,D6,D7):    
    string = '<hr/>\n'    
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Leu</font>cip<font color="DC143C">pus</font> - Atomic <font color="DC143C">Density</font> Explorer</h3>\n'
    string += '</p>\n'
    string += '<p>\n'
    string += 'This webpage interfaces with a C++ executable which calculates density maxima in ccp4 files from the PDBe. \n'
    string += '<i>Only valid for structures with ccp4 files stored on the ebi cloud. </i>\n'    
    string += ' </p>\n'

    string += '<hr/>\n'
    ############  BEGIN FORM ############################
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Maxima.cgi" accept-charset="UTF-8">\n'
    #Access Credentials
    string += '<b>~~ Application access credentials ~~</b>'
    string += '<br/><i>You must enter a valid email address to access this software. Passwords will be forthcoming.</i>'
    string += "<br/>Email address: <input type='text' name='email' value='" + username + "' />"
    string += " Password: <input type='text' name='password' value='not used' />"
    string += '<hr/>'
    #PDB code
    string +='<h3>Electron Density Analysis</h3>'
    string += 'Enter 4 digit pdb code: <input type="text" name="dataInput" value=' + pdb + ' />\n'    
    string += '<br/><br/>\n'
    #Data return format
    r1,r2,r3,r4,r5,r6,r7 = '','','','','','',''
    if D1:
        r1 = 'checked="checked"'
    if D2:
        r2 = 'checked="checked"'
    if D3:
        r3 = 'checked="checked"'
    if D4:
        r4 = 'checked="checked"'
    if D5:
        r5 = 'checked="checked"'
    if D6:
        r6 = 'checked="checked"'
    if D7:
        r7 = 'checked="checked"'


    string += '<table><tr><td style="background-color:Crimson;color:AliceBlue">~~ Choose results to display ~~</td>\n'
    string += '<td style="background-color:Crimson;color:AliceBlue"">~~ Calculation parameters ~~</td>\n'
    #string += '<td style="background-color:Crimson;color:AliceBlue"">~~ 3-point coordinates for plane ~~</td>\n'
    string += '</tr><tr><td>\n'
    string += '<table style="text-align: left;">\n'
    string += '<tr><td><label for="D1">1) Peaks visual projection to 3 planes</label></td><td><input type="checkbox" id="Data1" name="Data1" value="1" ' + r1 + '></td></tr>\n'
    string += '<tr><td><label for="D2">2) Peaks data in pseudo-pdb file</label></td><td><input type="checkbox" id="Data2" name="Data2" value="1" ' + r2 + '></td></tr>\n'
    string += '<tr><td><label for="D3">3) Peaks info as html grid</label></td><td><input type="checkbox" id="Data3" name="Data3" value="1" ' + r3 + '></td></tr>\n'
    string += '<tr><td><label for="D4">4) Peaks visual projection, atoms only (unit cell)</label></td><td><input type="checkbox" id="Data4" name="Data4" value="1" ' + r4 + '></td></tr>\n'
    string += '<tr><td><label for="D5">5) Density visual projection, all atoms</label></td><td><input type="checkbox" id="Data5" name="Data5" value="1" ' + r5 + '></td></tr>\n'
    string += '<tr><td><label for="D6">6) Atoms visualised on AtomNo</label></td><td><input type="checkbox" id="Data6" name="Data6" value="1" ' + r6 + '></td></tr>\n'
    #string += '<tr><td><label for="D7">7) Visualised electron density planes</label></td><td><input type="checkbox" id="Data7" name="Data7" value="1" ' + r7 + '></td></tr>\n'
    string += '</table>\n'
    string += '</td>'

    string += '<td><div style="text-align: left;">'


    #<p>Interpolation frequency: <input size="4" type="text" name="interpNum" value=' + str(interpNum) + ' /></p>'
    #string += '<p>Iterations per grid point, <br/>enter between 0 and 5, <br/>0 or 1 means grid points only</p>

    splinechecked = 'checked="checked"'
    nearestchecked = ''
    if interpMethod == "nearest":
        nearestchecked = 'checked="checked"'
        splinechecked = ''
        
    string += '<p><b>Interpolation:</b><br/>'
    string += '<input type="radio" id="spline" name="interpMethod" value="spline" ' + splinechecked + '><label for="spline">B-Spline</label><br/>'
    string += '<input type="radio" id="nearest" name="interpMethod" value="nearest" ' + nearestchecked + '><label for="nearest">Nearest Neighbour</label><br/>'
    string += '</p>'
    string += '<p><b>Fo and Fc numbers:</b><br/>\n'
    string += 'The main ccp4 file contains 2Fo-Fc<br/>\n'
    string += 'The diff file contains Fo-Fc<br/>\n'
    string += 'No Fos: <input type="text" name="Fos" value="' + Fos + '" size="2"/><br/>\n'
    string += 'No Fcs: <input type="text" name="Fcs" value="' + Fcs + '" size="2"/><br/>\n'
    string += '</p>\n'
    string += '</div></td>\n\n'
    #string += '<td><div style="text-align: left;"><b>Enter three points to get a density contour slice from the electron density.</b></div>\n'    
    #string += '<table style="background-color:AliceBlue;text-align:left;"><tr><td>Central: X=<input size="4" type="text" name="CX" value=' + str(cX) + ' />\n'
    #string += 'Y=<input size="4" type="text" name="CY" value=' + str(cY) + ' />\n'
    #string += 'Z=<input size="4" type="text" name="CZ" value=' + str(cZ) + ' /></td></tr>\n'
    #string += '<tr><td>Linear: X=<input size="4" type="text" name="LX" value=' + str(lX) + ' />\n'
    #string += 'Y=<input size="4" type="text" name="LY" value=' + str(lY) + ' />\n'
    #string += 'Z=<input size="4" type="text" name="LZ" value=' + str(lZ) + ' /></td></tr>\n'
    #string += '<tr><td>Planar: X=<input size="4" type="text" name="PX" value=' + str(pX) + ' />\n'
    #string += 'Y=<input size="4" type="text" name="PY" value=' + str(pY) + ' />\n'
    #string += 'Z=<input size="4" type="text" name="PZ" value=' + str(pZ) + ' /></td></tr></table>\n'
    #string += '<div style="text-align: left;padding:5px"><b>Settings for image size</b></div>\n'
    #string += '<table style="background-color:AliceBlue">\n'
    #string += '<tr>\n'
    #string += '<td>Width(&#8491;)=<input size="4" type="text" name="Width" value=' + str(width) + ' /> Granularity(&#8491;)=<input size="4" type="text" name="Gran" value=' + str(gran) + ' /></td>\n'
    string += '</tr>\n'
    string += '</table>\n'

    string += '</td></tr></table>\n'

    string += '<br/><input type="Submit" value="Analyse Electron Density"/>\n'    
    ############  END FORM ############################
    string += '</form>\n'
    string += '</div>\n'
    return string

def getBodyRun0(pdb):
    string = '<hr/>\n'
    string += '<h3>RESULTS: ' + pdb + '</h3>'        
    string += '<p>EBI Link <a class="change_link_color" href="https://www.ebi.ac.uk/pdbe/entry/pdb/' + pdb + '" title="EBI link" target="_blank">Open protein pdb ebi link</a></p>'
    return string
    
def getBodyRun1(pdb, dataABC, asCsv,D1,D2,D3,D4):
    string = ""
    if len(dataABC) > 0:
        dataA = dataABC[0]# peaks file
        dataB = dataABC[1]# peaks for atoms
        dataC = dataABC[2]# peaks for chimera            

        ### DATA 1 Peaks projection visualised #################################
        csvhtml=""
        if D1 or D2 or D3:
            csvhtml, csvtext = dataFrameToText(dataA)
            chimhtml, chimtext = dataFrameToText(dataC)
            savePeaksFile(pdb,csvtext,chimtext)
            
        if D1:
            string += '<hr/>\n'
            string += '<h4>1) Peaks visual projection to 3 planes</h4>'
            string += dataFrameToImages(pdb,dataA,"X","Y","Z","Density","cubehelix_r")            

        ### DATA 2 Peaks data as CSV #################################
        #-- https://www.w3schools.com/howto/tryit.asp?filename=tryhow_html_download_link --#
        
        if D2:
            pathname = 'https://student.cryst.bbk.ac.uk/~ab002/Peaks/peaks_' + pdb + '.ent'
            string += '<hr/>\n'
            #string += '<h4>2a) Peaks data as CSV file</h4>'
            #pathname = 'https://student.cryst.bbk.ac.uk/~ab002/Peaks/peaks_' + pdb + '.csv'            
            #string += csvhtml
            string += '<h4>2b) Peaks data in pseudo pdb file</h4>'            
            string += '<a class="change_link_color" href="' + pathname + '" download='+'peaks_'+pdb + '.ent >Download peaks pseudo pdb file</a><br/><br/>'
            string += chimhtml
            
        ### DATA 3 Peaks data as html grid #################################
        if D3:
            pathname = 'https://student.cryst.bbk.ac.uk/~ab002/Peaks/peaks_' + pdb + '.csv'            
            string += '<hr/>\n'
            string += '<h4>3) Peaks data as html grid</h4>'
            string += '<a class="change_link_color" href="' + pathname + '" download='+'peaks_'+pdb + '.csv >Download peaks info as csv file</a><br/><br/>'
            string += '<table><tr>'
            string += '<td style="background-color:silver;">Density</td>'
            string += '<td style="background-color:silver;">_ C _</td>'
            string += '<td style="background-color:silver;">_ R _</td>'
            string += '<td style="background-color:silver;">_ S _</td>'
            string += '<td style="background-color:silver;">_ X _</td>'
            string += '<td style="background-color:silver;">_ Y _</td>'
            string += '<td style="background-color:silver;">_ Z _</td>'
            string += '<td style="background-color:silver;">_______________ Nearest PDB Atom Line ______________</td>'
            string += '<td style="background-color:silver;">Distance</td>'
            string += '</tr></table>'
            string += dataFrameToGrid(dataA)

        ### DATA 4 Peaks projection atoms only #################################
        if D4:
            string += '<hr/>\n'
            string += '<h4>4) Peaks visual projection, atoms only (unit cell)</h4>'
            string += dataFrameToImages(pdb,dataB,"X","Y","Z","Density","cubehelix_r")
    else:
        string = '<font color="DC143C"><h1>Exe failed to create data</h1></font>'
    return string
    
def getBodyRun2(pdb, dataABC,D5,D6):
    string = ""
    if len(dataABC) > 0:        
        dataC = dataABC[0]
                        
        ### DATA 5 Density projection, all atoms #################################
        if D5:
            string += '<hr/>\n'
            string += '<h4>5) Density visual projection, all atoms</h4>'
            string += dataFrameToImages(pdb,dataC,"X","Y","Z","Density","cubehelix_r")

        ### DATA 6 Atom scatter plot, all atoms #################################
        if D6:
            string += '<hr/>\n'
            string += '<h4>6) Atoms visualised on AtomNo</h4>'
            string += dataFrameToImages(pdb,dataC,"X","Y","Z","AtomNo","gist_ncar")                    
    else:
        string = '<font color="DC143C"><h1>Exe failed to create data</h1></font>'
    return string
    

def dataFrameToImages(pdb,data,geoA,geoB,geoC,hue,palette):    
    mtx = createDummyMatrix()
    #string = matrixToImage(mtx)
    html = '<table style="table-layout:fixed;width:95%;display:block;display:table"><tr>'
    html += scatterToImage(pdb,data,hue,geoA,geoB,palette)
    html += scatterToImage(pdb,data,hue,geoB,geoC,palette)
    html += scatterToImage(pdb,data,hue,geoC,geoA,palette)
    html += '</tr></table>'
    
    return html
    

def scatterToMatrix(data,length,hue, cap):
    import math
    maxVal = data[hue].values.max()
    minVal = data[hue].values.min()
    maxCap = maxVal * cap
    real_len = len(data[hue].values)
    sq_len = int(math.sqrt(real_len))
    #print('lenghts',real_len,':',length)
    
    mtx = data[hue].values.reshape(int(sq_len),int(sq_len))
    for i in range(sq_len):
        for j in range(sq_len):
            if mtx[i,j] > maxCap:
                mtx[i,j] = maxCap
    return mtx, minVal
    

def addPosToMtx(mtx,length,minVal,data):
    
    for index,row in data.iterrows():        
        x = int(row['i'])
        y = int(row['j'])
        val = float(row['Position'])
        if x < length and y < length:
            mtx[x,y] = float(minVal-1)
    
    return mtx
            
    

def getBodyRun3(pdb,dataABC,width,gran,D7):
    ### DATA 6 Atom scatter plot, all atoms #################################
    string = ''
    if D7:
        length = (int)((float)(width)/(float)(gran))
        string += '<hr/>\n'
        string += '<h4>7) Visualised electron density planes</h4>'
        string += '<p>Width=' + str(width) + '&#8491; Granularity=' + str(gran) + '&#8491;'
        string += ' Sample data points =  ' + str(length+1) + 'x' + str(length+1) + '=' + str((length+1)*(length+1)) + '</p>'  
        if len(dataABC) > 0:
            havePos = False
            dataA = dataABC[0]
            dataB = dataABC[1]
            dataC = dataABC[2]
            dataD = pd.DataFrame()#The position data
            if len(dataABC) > 3:
                dataD = dataABC[3]
                havePos = True
            
            
            string += '<table style="table-layout:fixed;width:95%;display:block;display:table"><tr>'
            string += '<td style="width:33%;">Density</td><td style="width:33%;">Radiant</td><td style="width:33%;">Laplacian</td></tr><tr>'

            dContour = 0.3
            lContour = 0.2
            if pdb == "Synthetic":
                dContour = 0.8
                lContour = 0.4


            mtxD,minD = scatterToMatrix(dataA,length,'Density',dContour)
            mtxR,minR = scatterToMatrix(dataB,length,'Radiant',1)
            mtxL,minL = scatterToMatrix(dataC,length,'Laplacian',lContour)
            
            if havePos:
                mtxD = addPosToMtx(mtxD,length,minD,dataD)
                mtxR = addPosToMtx(mtxR,length,minR,dataD)
                mtxL = addPosToMtx(mtxL,length,minL,dataD)
            string += matrixToImage(pdb,mtxD,'magma_r',False,minD)
            string += matrixToImage(pdb,mtxR,'bone',False,minR)
            string += matrixToImage(pdb,mtxL,'magma',False,minL)

                                    
            string += '</tr></table>'

        else:
            string = '<font color="DC143C"><h1>Exe failed to create data</h1></font>'

    
    return string

def getBodyD(pdb,data,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ):
    string = '<hr/><h3>Visualised Electron Density</h3>\n'
    string += '<h3>SLICE RESULTS</h3>'
    mtx = createDummyMatrix()
    string += matrixToImage(mtx)
    return string


def getFooter():
    string = '<hr/>\n'
    string += '<p style="background-color:Crimson;margin:5px;padding:5px;color:AliceBlue;">\n'
    string += 'Created by: <a href = "mailto:ralcra01@student.bbk.ac.uk" > Rachel Alcraft </a >\n'
    string += ' ~ Home page: <a href="https://student.cryst.bbk.ac.uk/~ab002/Leucippus.html" title="Leucippus" target="_self">Leucippus</a>\n'
    string += ' ~ Supervisor: <a href="http://people.cryst.bbk.ac.uk/~ubcg66a/" title="MAW" target="_blank">Mark A. Williams</a>\n'
    string += ' ~ Birkbeck, University of London, 2021\n'
    string += '</p>\n'
    string += '</body>\n'
    return string

#Helper strings
def dataFrameToGrid(df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    cols = len(df.columns)
    rows = len(df.index)
    html = "<table style='max-height:450px;overflow-y: scroll;'>\n"
    html += "<tr class='verdinnerheader'>\n"
    for col in df.columns:
        html += "<td>" + col + "</td>\n"
    html += "</tr>\n"

    for c in range(0, rows):
        html += "<tr class='cppinnertable'>\n"
        for r in range(0, cols):
            val = df.iloc[c, r]
            try:
                val = round(val,6)
            except:
                val=val
            html += "<td>" + str(val) + "</td>\n"
        html += "</tr>\n"
    html += "</table>\n"
    return (html)

def dataFrameToText(df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    cols = len(df.columns)
    rows = len(df.index)
    html = "<TEXTAREA rows=20 cols=150>\n"
    text = ""
    
    row = ""
    for col in df.columns:
        row += "" + col + ","
    row = row[:len(row)-1]
    #row[len(row)-1] = "\n"
    html += row + "\n"
    text += row + "\n"

    for c in range(0, rows):
        row = ""
        for r in range(0, cols):
            val = df.iloc[c, r]
            try:
                val = round(val,6)
            except:
                val=val
            row += "" + str(val) + ","

        row = row[:len(row)-1]
        html += row + "\n"
        text += row + "\n"
    html += "</TEXTAREA>"
    return html,text

def savePeaksFile(pdb, text,text2):
    filename = '/d/user6/ab002/WWW/Peaks/peaks_' + pdb + '.csv'            
    if not os.path.isfile(filename) or True:#for now save it always while the format is changing TODO
        f = open(filename, "w")
        f.write(text)
        f.close()

    filename = '/d/user6/ab002/WWW/Peaks/peaks_' + pdb + '.ent'            
    if not os.path.isfile(filename) or True:
        f = open(filename, "w")
        f.write(text2)
        f.close()
    
    

def getPlotImage(fig, ax):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')    
    return encoded
    
def matrixToImage(pdb,mtx,pal,contour,minVal):
    fig, ax = plt.subplots()
    import matplotlib.cm as cm
    import copy

    cm2 = cm.get_cmap(pal)
    my_cmap = copy.copy(cm2)
    my_cmap.set_under('y')
    #mtx[10,10] = maxVal+1
        
    image = ax.imshow(mtx, cmap=my_cmap, interpolation='nearest', origin='lower', aspect='equal',alpha=1,vmin=minVal)
    if contour:
        image = plt.contour(mtx, colors='SlateGray', alpha=0.55, linewidths=0.3, levels=12)
    

    plt.axis('off')    
    encoded = getPlotImage(fig,ax)
    imstring = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
    #html = imstring        
    html = '<td style="width:33%;"><p>' + pdb + '</p><p>' + imstring + '</p></td>\n'
    return html


def scatterToImage(pdb, df, hue, xaxis,yaxis,pal):
    fig, ax = plt.subplots()
    
    df = df.sort_values(by=hue, ascending=True)
    count = len(df)
    
    g = ax.scatter(df[xaxis], df[yaxis], c=df[hue], cmap=pal,edgecolor='Silver', alpha=0.7,linewidth=0.8,s=20)
    cb = fig.colorbar(g)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    cb.set_label(hue)
    plt.title(pdb + ' Count=' + str(count))

    encoded = getPlotImage(fig,ax)
    imstring = '<img width=10% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
    #html = imstring
    html = ''
    html += '<td><p>' + str(xaxis) + '-' + str(yaxis) + ' by ' + hue + '</p>\n'
    html += '<p>' + imstring + '</p></td>\n'
    return html

def createDummyMatrix():
    vals2 = np.zeros([30,30])
    vals2[8,8] = 1
    vals2[9,9] = 1
    vals2[9,10] = 1
    vals2[10,10] = 2
    vals2[11,11] = 4
    vals2[12,11] = 3
    vals2[10,11] = 4
    vals2[10,11] = 5
    vals2[11,10] = 4
    vals2[20,20] = 2
    vals2[21,21] = 4
    vals2[22,21] = 8
    vals2[20,21] = 4
    vals2[20,21] = 5
    vals2[21,20] = 1
    vals2[14,14] = 6
    vals2[14,15] = 6
    vals2[14,16] = 6
    vals2[16,16] = 6
    vals2[15,14] = 6
    vals2[15,15] = 10
    vals2[15,16] = 10
    vals2[15,17] = 6
    vals2[16,13] = 6
    vals2[16,14] = 6
    vals2[16,17] = 6
    vals2[16,16] = 10
    vals2[16,15] = 10
    vals2[17,17] = 6
    vals2[18,17] = 6
    vals2[17,14] = 6
    vals2[17,15] = 3
    vals2[17,16] = 2
    vals2[4,14] = 6
    vals2[4,15] = 6
    vals2[4,16] = 6
    vals2[6,16] = 6
    vals2[5,14] = 6
    vals2[5,15] = 10
    vals2[5,16] = 10
    vals2[5,17] = 6
    vals2[6,14] = 6
    vals2[6,17] = 6
    vals2[6,16] = 10
    vals2[6,15] = 10
    vals2[7,17] = 6
    vals2[8,17] = 6
    vals2[7,14] = 6
    vals2[7,15] = 6
    vals2[7,16] = 6
    return vals2
