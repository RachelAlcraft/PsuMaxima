import Geometry.Geometry as geo
import PhdWebBuilder as pwb

#User inputs
pdbA = '3nir'
pdbB = '3nir'
pathA = 'C:/Dev/Github/ProteinDataFiles/pdb_data/'
pathB = 'C:/Dev/Github/ProteinDataFiles/pdb_out/LapDen_ADJ/Density/'
geoA = 'C:O'
geoB = 'C:N+1'
geoC = 'CA:C:N+1'
outputPath = "test.html"

html = pwb.getHeader(Geometry=True)#it has a different style
html += geo.innerStringTwoPdbCompare(pdbA,pdbB,pathA,pathB,geoA,geoB,geoC)
html += pwb.getFooter()
results = pwb.userOwnWebPage("RachelTest", html, True)






