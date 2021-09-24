#!/l_mnt/python/envs/teaching/bin/python3 
import pandas as pd
import sys
sys.path.append('/Geometry/')

import warnings
warnings.filterwarnings('ignore')

import Geometry.GeoReport as GR
import Geometry.GeoPdb as GP



def innerStringTwoPdbCompare(pdbA, pdbB, pathA, pathB, geoA, geoB, geoC):
    #print(pdbA, pdbB, geoA, geoB, geoC,pathA, pathB)
    geos = [geoA,geoB,geoC,'N:N']
    hueList = ['aa', 'rid', 'bfactor', 'pdbCode', 'bfactorRatio', 'disordered','occupancy']

    pdbmanager = GP.GeoPdbs(pathA, "", False, False, False, [])
    georep = GR.GeoReport([pdbA], pathA, "", "STRING", ed=False, dssp=False, includePdbs=False,keepDisordered=False)
    dataA = georep.getGeoemtryCsv(geos, hueList, -1, allAtoms=True)

    pdbmanager.clear()

    pdbmanager = GP.GeoPdbs(pathB, "", False, False, False, [])
    georep = GR.GeoReport([pdbB], pathB, "", "STRING", ed=False, dssp=False, includePdbs=False, keepDisordered=False)
    dataB = georep.getGeoemtryCsv(geos, hueList, -1, allAtoms=True)

    if pdbA == pdbB:
        pdbA = pdbA + '_1'
        pdbB = pdbB + '_2'
        dataA['pdbCode'] = dataA['pdbCode'] + "_1"
        dataB['pdbCode'] = dataB['pdbCode'] + "_2"

    dataA['rid'] = dataA['rid'].astype(str)
    dataB['rid'] = dataB['rid'].astype(str)

    dataA['ID'] = dataA['aa'] + dataA['rid']
    dataB['ID'] = dataB['aa'] + dataB['rid']

    dataA['pdb'] = dataA['N:N']
    dataB['N:N'] = dataB['N:N']+1

    

    #dataA['pdb'] = dataA['pdb'].astype(int)
    #dataA['pdb'] = dataA['pdb'].astype(int)

    dataC = pd.concat([dataA, dataB], ignore_index=False)

    georep.addHistogram(data=dataA, geoX=geoA, title=pdbA + ':' + geoA,hue='ID')
    georep.addHistogram(data=dataA, geoX=geoB, title=pdbA + ':' + geoB,hue='ID')
    georep.addHistogram(data=dataA, geoX=geoC, title=pdbA + ':' + geoC,hue='ID')

    georep.addHistogram(data=dataB, geoX=geoA, title=pdbA + ':' + geoA,hue='ID')
    georep.addHistogram(data=dataB, geoX=geoB, title=pdbA + ':' + geoB,hue='ID')
    georep.addHistogram(data=dataB, geoX=geoC, title=pdbA + ':' + geoC,hue='ID')

    georep.addScatter(data=dataA,geoX=geoA,geoY=geoB,hue=geoC,title=pdbA+':'+geoA+':'+geoB,categorical=False, palette='viridis_r',sort='RAND',ghost=False)
    georep.addScatter(data=dataA,geoX=geoB,geoY=geoC,hue=geoA,title=pdbA+':'+geoB+':'+geoC,categorical=False, palette='viridis_r', sort='RAND',ghost=False)
    georep.addScatter(data=dataA,geoX=geoC,geoY=geoA,hue=geoB,title=pdbA+':'+geoC+':'+geoA,categorical=False, palette='viridis_r', sort='RAND',ghost=False)

    georep.addScatter(data=dataB, geoX=geoA, geoY=geoB, hue=geoC, title=pdbB + ':' + geoA + ':' + geoB,categorical=False, palette='viridis_r', sort='RAND',ghost=False)
    georep.addScatter(data=dataB, geoX=geoB, geoY=geoC, hue=geoA, title=pdbB + ':' + geoB + ':' + geoC,categorical=False, palette='viridis_r', sort='RAND',ghost=False)
    georep.addScatter(data=dataB, geoX=geoC, geoY=geoA, hue=geoB, title=pdbB + ':' + geoC + ':' + geoA,categorical=False, palette='viridis_r', sort='RAND',ghost=False)

    georep.addScatter(data=dataC, geoX=geoA, geoY=geoB, hue='N:N', title=pdbA + '=yellow,' + pdbB + '=Purple',categorical=True, palette='viridis_r', sort='RAND',ghost=False)
    georep.addScatter(data=dataC, geoX=geoB, geoY=geoC, hue='N:N', title=pdbA + '=yellow,' + pdbB + '=Purple',categorical=True, palette='viridis_r', sort='RAND',ghost=False)
    georep.addScatter(data=dataC, geoX=geoC, geoY=geoA, hue='N:N', title=pdbA + '=yellow,' + pdbB + '=Purple',categorical=True, palette='viridis_r', sort='RAND',ghost=False)
    #georep.addScatter(data=dataC, geoX=geoB, geoY=geoC, hue='pdbe', title=geoB + ':' + geoC,categorical=False, palette='jet_r', sort='RAND',ghost=False)
    #georep.addScatter(data=dataC, geoX=geoC, geoY=geoA, hue='pdbe', title=geoC + ':' + geoA,categorical=False, palette='jet_r', sort='RAND',ghost=False)

    string = georep.printToHtml('Rachel', 3, "STRING")
    return string


