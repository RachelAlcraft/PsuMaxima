
import pandas as pd
import math

def getCsvFromCppResults_Slices(fileName):
    dataResults = {}
    #First load up as a big string
    text_file = open(fileName, "r")
    cpp_data = text_file.read()
    text_file.close()# close file

    startPos = cpp_data.find('BEGIN_SLICENUMS') + len('BEGIN_SLICENUMS')
    endPos = cpp_data.find('END_SLICENUMS')
    print(startPos,endPos)
    if endPos > startPos:
        numSlices = (cpp_data[startPos:endPos]).strip()
        print(numSlices)
        df = pd.DataFrame([numSlices])
        dataResults['SLICENUMS'] = df

        for i in range(int(numSlices)):
            datalst = []
            ID_start = 'BEGIN_DENSITYSLICE_' + str(i)
            startPos = cpp_data.find(ID_start) + len(ID_start)
            ID_end = 'END_DENSITYSLICE_' + str(i)
            endPos = cpp_data.find(ID_end)
            print(i,ID_start,startPos,endPos)
            data = (cpp_data[startPos:endPos]).strip()
            datalsta = data.split('\n')
            firstRow = True
            for row in datalsta:
                if not firstRow:
                    lst = row.split(',')
                    datalst.append(lst)
                firstRow=False
            df = pd.DataFrame(datalst, columns=['i', 'j', 'Density'])
            dataResults['DENSITYSLICE_' + str(i)] = df


    print(dataResults['DENSITYSLICE_0'])
    return int(numSlices), dataResults


def DataFrameToMatrix(data, hue):
    real_len = len(data[hue].values)
    sq_len = int(math.sqrt(real_len))
    mtx = data[hue].values.reshape(int(sq_len), int(sq_len))
    return mtx


