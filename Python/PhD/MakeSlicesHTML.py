
import FilesAndCSVs as fac
from PsuGeometry import GeoReport as psu

leuFileName = 'C:/Dev/Github/ProteinDataFiles/LeicippusTesting/Analysis/7a6a_SLICESFILE.csv'

numSlices, results = fac.getCsvFromCppResults_Slices(leuFileName)
slices = []

for i in range(numSlices):
    ID = 'DENSITYSLICE_' + str(i)
    df = results[ID]
    mtx = fac.DataFrameToMatrix(df,'Density')
    slices.append[mtx]



pdbDataPath = 'C:/Dev/Github/ProteinDataFiles/LeicippusTesting/PdbFiles/'
edDataPath = 'C:/Dev/Github/ProteinDataFiles/ccp4_data/'
printPath = 'C:/Dev/Github/ProteinDataFiles/LeicippusTesting/Analysis/'

georep = psu.GeoReport([],pdbDataPath,edDataPath,printPath,ed=True,dssp=True)