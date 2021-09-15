
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
    res += '<p><i>This is your private results page, further results will be copied here, it will not be stored on the server so save as needed<i><p>'
    
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
    string += '<title>PsuMaxima</title>\n'   
    string += '<link rel="icon" href="/../../../~ab002/img/atom.ico" type="image/x-icon">\n'         
    string += '<style>\n'
    string += 'body {text-align:left;background-color:LightSteelBlue;margin-left: 52px;}\n'
    string += 'img {width:85%;border:1px solid MistyRose; }\n'
    #string += 'table {font-size:0.8vw;width:95%;table-layout:fixed;display:table;margin:0 auto;background-color:LightSteelBlue ;}\n'
    #string += 'table {table-layout:fixed; text-align: center; border: 0.5px solid MistyRose; background: LightSteelBlue; padding: 0px; max-height:450px; overflow-y: scroll;  display: block;table-layout:fixed;}\n'
    string += 'table {table-layout:fixed; text-align: center; border: 0.5px solid MistyRose; background: LightSteelBlue; padding: 0px;display: block;table-layout:fixed;}\n'
    string += 'td {padding:2px;border:0.5px solid rgb(180, 180, 280,0.75);background-color:AliceBlue;}\n' 
    #string += '.verdtable {table-layout:fixed; text-align: left; border: 3px solid RebeccaPurple; background: MistyRose; padding: 0px; max-height: 250px; overflow-y: scroll;  display: block;}'
    #string += '.verdinnerheader td {border: 3px solid RebeccaPurple;background: RebeccaPurple;padding: 0px; color: Chartreuse;}'
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
    string += '<p style="background-color:Crimson;margin:5px;padding:5px;color:AliceBlue;">'
    string += '<a href="/../../~ab002/Maxima.html" title="Home" target="_self">PhD Home</a>'
    string += "~ <a href='/../../~ab002/index.html' title='Student' target='_blank'>Student Home</a>"
    string += "~ <a href='https://www.bbk.ac.uk/departments/biology/' title='Birkbeck' target='_blank'>Birkbeck Biology</a>"
    string += '</p>'
    
    return string



def getBodyA(pdb, dataAsCsv, username, password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ,width,gran,D1,D2,D3,D4,D5,D6,D7):    
    string = '<hr/>\n'
    string += '<h1>\n'
    string += '<font color="DC143C">Psu</font>Max<font color="DC143C">ima</font>\n'
    string += '</h1>\n'
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Psu</font>Max<font color="DC143C">ima</font></h3>\n'
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


    string += '<table><tr><td style="background-color:Crimson;color:AliceBlue">~~ Choose results to display ~~</td><td style="background-color:Crimson;color:AliceBlue"">~~ 3-point coordinates for plane ~~</td></tr><tr>\n'
    string += '<td>\n'
    string += '<table style="text-align: left;">\n'
    string += '<tr><td><label for="D1">1) Peaks visual projection to 3 planes</label></td><td><input type="checkbox" id="Data1" name="Data1" value="1" ' + r1 + '"></td></tr>\n'
    string += '<tr><td><label for="D2">2) Peaks data as CSV file</label></td><td><input type="checkbox" id="Data2" name="Data2" value="1" ' + r2 + '"></td></tr>\n'
    string += '<tr><td><label for="D3">3) Peaks data as html grid</label></td><td><input type="checkbox" id="Data3" name="Data3" value="1" ' + r3 + '"></td></tr>\n'
    string += '<tr><td><label for="D4">4) Peaks visual projection, atoms only (unit cell)</label></td><td><input type="checkbox" id="Data4" name="Data4" value="1" ' + r4 + '"></td></tr>\n'
    string += '<tr><td><label for="D5">5) Density visual projection, all atoms</label></td><td><input type="checkbox" id="Data5" name="Data5" value="1" ' + r5 + '"></td></tr>\n'
    string += '<tr><td><label for="D6">6) Atoms visualised on AtomNo</label></td><td><input type="checkbox" id="Data6" name="Data6" value="1" ' + r6 + '"></td></tr>\n'
    string += '<tr><td><label for="D7">7) Visualised electron density planes</label></td><td><input type="checkbox" id="Data7" name="Data7" value="1" ' + r7 + '"></td></tr>\n'
    string += '</table>\n'
    string += '</td><td>\n'
    string += '<div style="text-align: left;"><b>Enter three points to get a density contour slice from the electron density.</b></div>\n'    
    string += '<table style="background-color:AliceBlue;text-align:left;"><tr><td>Central: X=<input type="text" name="CX" value=' + str(cX) + ' />\n'
    string += 'Y=<input type="text" name="CY" value=' + str(cY) + ' />\n'
    string += 'Z=<input type="text" name="CZ" value=' + str(cZ) + ' /></td></tr>\n'
    string += '<tr><td>Linear: X=<input type="text" name="LX" value=' + str(lX) + ' />\n'
    string += 'Y=<input type="text" name="LY" value=' + str(lY) + ' />\n'
    string += 'Z=<input type="text" name="LZ" value=' + str(lZ) + ' /></td></tr>\n'
    string += '<tr><td>Planar: X=<input type="text" name="PX" value=' + str(pX) + ' />\n'
    string += 'Y=<input type="text" name="PY" value=' + str(pY) + ' />\n'
    string += 'Z=<input type="text" name="PZ" value=' + str(pZ) + ' /></td></tr></table>\n'

    string += '<div style="text-align: left;padding:5px"><b>Settings for image size</b></div>\n'
    string += '<table style="background-color:AliceBlue">\n'
    string += '<tr>\n'
    string += '<td>Width(&#8491;)=<input type="text" name="Width" value=' + str(width) + ' /> Granularity(&#8491;)=<input type="text" name="Gran" value=' + str(gran) + ' /></td>\n'
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
    
def getBodyRun1(pdb, dataABC, asCsv,D1,D2,D3):
    string = ""
    if len(dataABC) > 0:
        dataA = dataABC[0]
        dataB = dataABC[1]
        dataC = dataABC[2]            

        ### DATA 1 Peaks projection visualised #################################
        csvhtml=""
        if D1 or D2 or D3:
            csvhtml, csvtext = dataFrameToText(dataA)
            savePeaksFile(pdb,csvtext)
            
        if D1:
            string += '<hr/>\n'
            string += '<h4>1) Peaks visual projection to 3 planes</h4>'
            string += dataFrameToImages(pdb,dataA,"X","Y","Z","Density","cubehelix_r")            

        ### DATA 2 Peaks data as CSV #################################
        #-- https://www.w3schools.com/howto/tryit.asp?filename=tryhow_html_download_link --#
        if D2:
            string += '<hr/>\n'
            string += '<h4>2) Peaks data as CSV file</h4>'
            pathname = 'https://student.cryst.bbk.ac.uk/~ab002/Peaks/peaks_' + pdb + '.csv'
            string += '<a class="change_link_color" href="' + pathname + '" download='+'peaks_'+pdb + '.csv >Download peaks file</a><br/><br/>'
            string += csvhtml
            
        ### DATA 3 Peaks data as html grid #################################
        if D3:
            string += '<hr/>\n'
            string += '<h4>3) Peaks data as html grid</h4>'
            string += dataFrameToGrid(dataA)    
    else:
        string = '<font color="DC143C"><h1>Exe failed to create data</h1></font>'
    return string
    
def getBodyRun2(pdb, dataABC, D4,D5,D6):
    string = ""
    if len(dataABC) > 0:
        dataA = dataABC[0]
        dataB = dataABC[1]
        dataC = dataABC[2]
                
        ### DATA 4 Peaks projection atoms only #################################
        if D4:
            string += '<hr/>\n'
            string += '<h4>4) Peaks visual projection, atoms only (unit cell)</h4>'
            string += dataFrameToImages(pdb,dataB,"X","Y","Z","Density","cubehelix_r")

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
    maxVal = data[hue].values.max()
    maxCap = maxVal * cap  
    try:
        mtx = data[hue].values.reshape(length+1,length+1)
        for i in range(length+1):
            for j in range(length+1):
                if mtx[i,j] > maxCap:
                    mtx[i,j] = maxCap
        return mtx
    except:
        return np.zeros([3,3])
            
    

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
            dataA = dataABC[3]
            dataB = dataABC[4]
            dataC = dataABC[5]
            
            
            string += '<table style="table-layout:fixed;width:95%;display:block;display:table"><tr>'
            string += '<td style="width:33%;">Density</td><td style="width:33%;">Radiant</td><td style="width:33%;">Laplacian</td></tr><tr>'

            mtxD = scatterToMatrix(dataA,length,'Density',0.3)
            mtxR = scatterToMatrix(dataB,length,'Radiant',1)
            mtxL = scatterToMatrix(dataC,length,'Laplacian',0.3)        
            string += matrixToImage(pdb,mtxD,'magma_r',False)
            string += matrixToImage(pdb,mtxR,'bone',False)
            string += matrixToImage(pdb,mtxL,'magma',False)

            #string += scatterToImage(pdb,dataA,"Density","i","j","inferno")
            #string += scatterToImage(pdb,dataB,"Radiant","i","j","inferno")
            #string += scatterToImage(pdb,dataC,"Laplacian","i","j","inferno")
            
            
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
    string += 'Created by: Rachel Alcraft<br/>\n'
    string += '<a href="https://student.cryst.bbk.ac.uk/~ab002/" title="PhDBio" target="_blank">Birkbeck Student Page - Rachel Alcraft</a>\n'
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

def savePeaksFile(pdb, text):
    filename = '/d/user6/ab002/WWW/Peaks/peaks_' + pdb + '.csv'            
    if not os.path.isfile(filename) or True:#for now save it always while the format is changing TODO
        f = open(filename, "w")
        f.write(text)
        f.close()
    
    

def getPlotImage(fig, ax):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')    
    return encoded
    
def matrixToImage(pdb,mtx,pal,contour):
    fig, ax = plt.subplots()
    image = plt.imshow(mtx, cmap=pal, interpolation='nearest', origin='lower', aspect='equal',alpha=1)
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
