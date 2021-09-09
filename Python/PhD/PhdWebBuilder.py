
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def userSuccess(email,password):
    isok = True
    #Does the email address contaion an @ sign?
    on_at = email.split('@')
    if len(on_at) != 2:
        isok = False
    on_dot = email.split('.')
    if len(on_dot) <2:
        isok = False

    if isok:
        directory = '/d/projects/u/ab002/Thesis/PhD/Data/Users/'
        filename = email
        from datetime import datetime
        dateTimeObj = datetime.now()
        dateObj = dateTimeObj.date()
        timestampStr = dateTimeObj.strftime("_%d_%b_%Y_%H_%M_%S_%f")
        filename += timestampStr + ".txt"
        f = open(directory+filename, "w")
        f.write("")
        f.close()
        
  
  
  
    
    return isok

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
    string += '</style></head>\n'

    # header includes a bit of body, where we have the header...
    string += '<body>\n'
    string += '<hr/>'
    string += '<p style="background-color:Crimson;margin:5px;padding:5px;color:AliceBlue;">'
    string += '<a href="/../../~ab002/Maxima.html" title="Home" target="_self">PhD Home</a>'
    string += "~ <a href='/../../~ab002/index.html' title='Student' target='_blank'>Student home</a>"
    string += "~ <a href='https://www.bbk.ac.uk/departments/biology/' title='Birkbeck' target='_blank'>Birkbeck Biology</a>"
    string += '</p>'
    
    return string



def getBodyA(pdb, dataAsCsv, username, password,cX,cY,cZ,lX,lY,lZ,pX,pY,pZ):    
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
    string += 'The results include:\n'
    string += '<li>Visualisation of projected density peaks in 3 planes: XY, YZ and ZX</li>\n'
    string += '<li>The density peaks in sorted order, including CRS and XYZ coordinates, with nearest atoms</li>\n'
    string += '<li>Another visualisation of peaks, but this time only those with a nearby atom (unit cell)</li>\n'
    string += '<li>Another density unit cell visualisation, this time the density of all the atoms (peak or not)</li>\n'
    string += '<li>All the atoms with a hue of AtomNo, to assist with mental disentangling of the chains</li>\n'
    string += '<li><font color=grey>For 3 given points, the planar slices of density, radiant and laplacian (not yet...)</font></li>\n'
    string += ' </p>\n'

    string += '<hr/>\n'
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Maxima.cgi" accept-charset="UTF-8">\n'
    #Access Credentials
    string += '~~ Application access credentials ~~'
    string += '<br/><i>You must enter a valid email address to access this software. Passwords will be forthcoming.</i>'
    string += "<br/>Email address: <input type='text' name='email' value='" + username + "' />"
    string += " Password: <input type='text' name='password' value='not used' />"
    string += '<hr/>'
    #PDB code
    string +='<h3>Electron Density Analysis</h3>'
    string += 'Enter 4 digit pdb code: <input type="text" name="dataInput" value=' + pdb + ' />\n'    
    string += '<br/>Choose data format: \n'
    #Data return format
    csv = 'checked'
    grid = ''
    if not dataAsCsv:
        csv = ''
        grid = 'checked'
    string += '<input type="radio" id="asCsv" name="format" value="asCsv" ' + csv +' ><label for="asCsv">As csv file</label>'
    string += '<input type="radio" id="asGrid" name="format" value="asGrid" '+ grid +' ><label for="asGrid">As grid</label>'
    #Coordinates for the slice
    string += '<p>Three points are needed for a plane. Enter three points to get a density contour slice from the electron density.'
    string += '<br/> !!! Results are currently dummy !!!</p>\n'

    string += '<table><tr><td>Central: X=<input type="text" name="CX" value=' + str(cX) + ' />\n'
    string += ' Y=<input type="text" name="CY" value=' + str(cY) + ' />\n'
    string += ' Z=<input type="text" name="CZ" value=' + str(cZ) + ' /></td></tr>\n'

    string += '<tr><td>Linear: X=<input type="text" name="LX" value=' + str(lX) + ' />\n'
    string += ' Y=<input type="text" name="LY" value=' + str(lY) + ' />\n'
    string += ' Z=<input type="text" name="LZ" value=' + str(lZ) + ' /></td></tr>\n'

    string += '<tr><td>Planar: X=<input type="text" name="PX" value=' + str(pX) + ' />\n'
    string += ' Y=<input type="text" name="PY" value=' + str(pY) + ' />\n'
    string += ' Z=<input type="text" name="PZ" value=' + str(pZ) + ' /></td></tr></table>\n'

    string += '<br/><input type="Submit" value="Analyse"/>\n'
    string += '</form>\n'
    string += '</div>\n'
    return string

def getBodyB(pdb, dataABC, asCsv):

    if len(dataABC) > 0:
        dataA = dataABC[0]
        dataB = dataABC[1]
        dataC = dataABC[2]

        string = '<hr/>\n'
        string += '<p>EBI Link <a href="https://www.ebi.ac.uk/pdbe/entry/pdb/' + pdb + '" title="EBI link" target="_blank">Open protein pdb ebi link</a></p>'

        string += '<hr/>\n'
        string += '<h3>MAXIMA RESULTS</h3>'

        string += '<p>' + pdb + ': Peaks projections</p>'
        string += dataFrameToImages(pdb,dataA,"X","Y","Z","Density","cubehelix_r")

        if not asCsv:
            string += '<p>' + pdb + ': Peaks grid </p>'
            string += dataFrameToGrid(dataA)
        else:
            string += '<p>' + pdb + ': Peaks csv file </p>'
            string += dataFrameToText(dataA)

        string += '<p>' + pdb + ': Atom only peaks projections</p>'
        string += dataFrameToImages(pdb,dataB,"X","Y","Z","Density","cubehelix_r")

        string += '<p>' + pdb + ': Pdb atoms density projections</p>'
        string += dataFrameToImages(pdb,dataC,"X","Y","Z","Density","cubehelix_r")

        string += '<p>' + pdb + ': Pdb atoms on atom no</p>'
        string += dataFrameToImages(pdb,dataC,"X","Y","Z","AtomNo","jet")
    else:
        string = '<font color="DC143C"><h1>Exe failed to create data</h1></font>'


    
    
    
    return string
    
    
def dataFrameToImages(pdb,data,geoA,geoB,geoC,hue,palette):    
    mtx = createDummyMatrix()
    #string = matrixToImage(mtx)
    html = '<table><tr>'
    html += scatterToImage(pdb,data,hue,geoA,geoB,palette)
    html += scatterToImage(pdb,data,hue,geoB,geoC,palette)
    html += scatterToImage(pdb,data,hue,geoC,geoA,palette)
    html += '</tr></table>'
    
    return html
    

def scatterToMatrix(data,length,hue):
    try:
        mtx = data[hue].values.reshape(length+1,length+1)
        return mtx
    except:
        return np.zeros([3,3])
            
    

def getBodyC(pdb,dataABC):
    
    if len(dataABC) > 0:
        dataA = dataABC[3]
        dataB = dataABC[4]
        dataC = dataABC[5]

        string = '<hr/>\n'
        string = '<hr/><h3>Visualised Electron Density</h3>\n'
        string += '<h3>SLICE RESULTS</h3>'
        
        string += '<table><tr>'
        string += '<td>Density</td><td>Radiant</td><td>Laplacian</td></tr><tr>'

        mtxD = scatterToMatrix(dataA,50,'Density')
        mtxR = scatterToMatrix(dataB,50,'Radiant')
        mtxL = scatterToMatrix(dataC,50,'Laplacian')        
        string += matrixToImage(pdb,mtxD)
        string += matrixToImage(pdb,mtxR)
        string += matrixToImage(pdb,mtxL)

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
    string += '<div id="bottom">\n'
    string += '<p>\n'
    string += 'Created by: Rachel Alcraft<br/>\n'
    string += '<a href="https://student.cryst.bbk.ac.uk/~ab002/" title="PhDBio" target="_blank">Birkbeck Student Page - Rachel Alcraft</a>\n'
    string += '</p>\n'
    string += '</div>\n'
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
    
    row = ""
    for col in df.columns:
        row += "" + col + ","
    row = row[:len(row)-1]
    #row[len(row)-1] = "\n"
    html += row + "\n"

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
    html += "</TEXTAREA>"
    return (html)

def getPlotImage(fig, ax):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')    
    return encoded
    
def matrixToImage(pdb,mtx):
    fig, ax = plt.subplots()
    image = plt.imshow(mtx, cmap='inferno', interpolation='nearest', origin='lower', aspect='equal',alpha=1)        
    image = plt.contour(mtx, colors='SlateGray', alpha=0.55, linewidths=0.3, levels=12)
    plt.axis('off')    
    encoded = getPlotImage(fig,ax)
    imstring = '<img width=10% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
    #html = imstring        
    html = '<td><p>' + pdb + '</p><p>' + imstring + '</p></td>\n'
    return html


def scatterToImage(pdb, df, hue, xaxis,yaxis,pal):
    fig, ax = plt.subplots()
    
    df = df.sort_values(by=hue, ascending=True)
    count = len(df)
    
    g = ax.scatter(df[xaxis], df[yaxis], c=df[hue], cmap=pal,edgecolor='AliceBlue', alpha=0.7,linewidth=0.8,s=20)
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
