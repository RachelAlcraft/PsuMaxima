
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


def getHeader():
    string = '<!DOCTYPE html>\n'
    string += '<html lang="en">\n'
    string += '<head>\n'
    string += '<title>PsuMaxima</title>\n'   
    string += '<link rel="icon" href="/../../../~ab002/img/atom.ico" type="image/x-icon">\n'         
    string += '<style>\n'
    string += 'body {text-align:left;background-color:LightSteelBlue;margin-left: 52px;}\n'
    string += 'img {width:55%;border:1px solid MistyRose; }\n'
    string += 'table {font-size:0.8vw;width:95%;table-layout:fixed;display:table;margin:0 auto;background-color:LightSteelBlue ;}\n'
    string += 'td {border:1px solid MistyRose;background-color:AliceBlue;}</style>\n'
    string += '</head>\n'
    return string



def getBodyA():
    string = '<body>\n'
    string += '<hr/>\n'
    string += '<h1>\n'
    string += '<font color="DC143C">Psu</font>Max<font color="DC143C">ima</font>\n'
    string += '</h1>\n'
    string += '<p>\n'
    string += '<h3>PhD project: <font color="DC143C">Psu</font>Max<font color="DC143C">ima</font></h3>\n'
    string += '</p>\n'
    string += '<p>\n'
    string += 'This webpage interfaces with a C++ executable which calculates density maxima in ccp4 files from the PdbE. Enter the pdb code for the results.\n'
    string += '</p>\n'
    string += '<hr/>\n'
    string += '<div class="middle">\n'
    string += '<p>\n'
    string += 'Enter 4 digit pdb code:\n'
    string += '</p>\n'
    string += '<form method="post" action="/cgi-bin/cgiwrap/ab002/PhD/Maxima.cgi" accept-charset="UTF-8">\n'
    string += '<p><input type="text" name="dataInput"/>\n'
    string += '<input type="Submit" value="Analyse"/>\n'
    string += '</form>\n'
    string += '</div>\n'
    return string

def getBodyB(pdb, data):
    string = '<hr/>\n'
    string += '<h3>MAXIMA RESULTS</h3>'
    string += '<p>' + pdb + '</p>'
    string += dataFrameToGrid(data)
    return string
    
def getBodyC():
    string = '<p>Instructions here to enter coordinates for a density slice, results currently dummy</p>\n'
    string += '<h3>SLICE RESULTS</h3>'
    return string
    
def getBodyD(pdb, data):    
    mtx = createDummyMatrix()
    string = matrixToImage(mtx)
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
    html = "<table class='cpptable'>\n"
    html += "<tr class='cppinnerheader'>\n"
    for col in df.columns:
        html += "<td>" + col + "</td>\n"
    html += "</tr>\n"

    for c in range(0, rows):
        html += "<tr class='cppinnertable'>\n"
        for r in range(0, cols):
            html += "<td>" + str((df.iloc[c, r])) + "</td>\n"
        html += "</tr>\n"
    html += "</table>\n"
    return (html)

def getPlotImage(fig, ax):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')    
    return encoded
    
def matrixToImage(mtx):
    fig, ax = plt.subplots()
    image = plt.imshow(mtx, cmap='cubehelix_r', interpolation='nearest', origin='lower', aspect='equal',alpha=1)        
    image = plt.contour(mtx, colors='SlateGray', alpha=0.55, linewidths=0.3, levels=12)
    plt.axis('off')
    encoded = getPlotImage(fig,ax)
    imstring = '<img width=10% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
    #html = imstring
    html = '<table><tr>'
    html += '<td>Coords entered here</td>'
    html += '<td>' + '<p>' + imstring + '</p></td></tr></table>\n'
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
