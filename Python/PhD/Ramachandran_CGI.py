#!/l_mnt/python/envs/teaching/bin/python3
import sys
#sys.path.append('/d/user6/ab002/WWW/cgi-bin/PhD/Geometry/')
sys.path.append('/Geometry/')
import Geometry.Geometry as geo
import PhdWebBuilder as pwb

import Bio.PDB as bio
import seaborn as sns

#User inputs
pdbA = '3nir'
pathA = 'C:/Dev/Github/ProteinDataFiles/pdb_data/'
pathB = 'C:/Dev/Github/ProteinDataFiles/pdb_out/LapDen_ADJ/Density/'
hueA = 'N:CA'

html = pwb.getHeader(Geometry=True)#it has a different style
html += geo.innerStringRamachandran(pdbA,pathA,hueA)
html += pwb.getFooter()
results = pwb.userOwnWebPage("RachelTest", html, True)






