'''
Author: Rachel Alcraft
Date: 01/09/2020
Description:
A very light class designed to hold the data required for PdbGeometry per atom
Note that the residue info is stored in the atom for simplicity
'''

class GeoAtom:

    def __init__(self):
        # this defines the data we allow in the atom
        # Structure information
        self.values = {}
        self.values['pdbCode'] = ''
        self.values['resolution'] = 0
        # Residue information
        self.values['chain'] = ''
        self.values['rid'] = 0
        self.values['ridx'] = 0
        self.values['dssp'] = ''
        self.values['aa'] = ''
        # Atom information
        self.values['atom'] = ''
        self.values['atomNo'] = 0
        self.values['x'] = 0
        self.values['y'] = 0
        self.values['z'] = 0
        self.values['bfactor'] = 0
        self.values['bfactorRatio'] = 0
        self.values['disordered'] = 'N'
        self.values['occupant'] = ''
        self.values['occupancy'] = 0
        self.values['electrons'] = ''
        self.values['element'] = ''
        # Density information
        self.values['Fo'] = 0
        self.values['Fc'] = 0
        self.values['FoFc'] = 0
        self.values['2FoFc'] = 0


    def __str__(self):
        return self.values['pdbCode'] + '_'+self.values['atom']+'_'+str(self.values['atomNo'])+'_'+str(self.values['rid'])+'_'+self.values['aa']+'_'+self.values['occupant']

    def setStructureInfo(self,pdbCode,resolution):
        self.values['pdbCode'] = pdbCode
        self.values['resolution'] = resolution

    def setResidueInfo(self,chain,rid,ridx,aa):
        self.values['chain'] = chain
        self.values['rid'] = int(rid)
        self.values['ridx'] = int(ridx)
        self.values['aa'] = aa

    def setAtomInfo(self,residue,atom,atomNo,x,y,z,bfactor,occupant,occupancy,disordered):
        self.values['residue'] = residue
        self.values['atom'] = atom
        self.values['atomNo'] = int(atomNo)
        self.values['x'] = x
        self.values['y'] = y
        self.values['z'] = z
        self.values['bfactor'] = bfactor
        self.values['disordered'] = disordered
        self.values['occupant'] = occupant
        self.values['occupancy'] = occupancy
        self.values['electrons'] = self.getElectrons(atom)
        self.values['element'] = self.getElement(atom)

    def setDsspInfo(self,dssp):
        self.values['dssp'] = dssp

    def setDensityInfo(self,tFoFc,FoFc,Fo,Fc):
        self.values['2FoFc'] = tFoFc
        self.values['FoFc'] = FoFc
        self.values['Fo'] = Fo
        self.values['Fc'] = Fc


    def getElectrons(self,atom):
        if 'CL' in atom:
            return 17
        elif 'P' in atom:
            return 15
        elif 'AL' in atom:
            return 13
        elif 'FE' in atom:
            return 26
        elif 'CO' in atom:
            return 27
        elif 'CR' in atom:
            return 24
        elif 'MN' in atom:
            return 25
        elif 'NA' in atom:
            return 11
        elif 'MG' in atom:
            return 12
        elif 'BR' in atom:
            return 35
        elif 'AU' in atom:
            return 79
        elif 'C' in atom:
            return 6
        elif 'K' in atom:
            return 19
        elif 'F' in atom:
            return 9
        elif 'S' in atom:
            return 16
        elif 'N' in atom:
            return 7
        elif 'O' in atom:
            return 8
        elif 'H' in atom:
            return 1
        elif 'D' in atom: # deuterium
            return 2
        else:
            return 100

    def getElement(self,atom):
        if 'CL' in atom:
            return 'CL'
        elif 'P' in atom:
            return 'P'
        elif 'AL' in atom:
            return 'AL'
        elif 'FE' in atom:
            return 'FE'
        elif 'CO' in atom:
            return 'CO'
        elif 'CR' in atom:
            return 'CR'
        elif 'MN' in atom:
            return 'MN'
        elif 'NA' in atom:
            return 'NA'
        elif 'MG' in atom:
            return 'MG'
        elif 'BR' in atom:
            return 'BR'
        elif 'AU' in atom:
            return 'AU'
        elif 'C' in atom:
            return 'C'
        elif 'K' in atom:
            return 'K'
        elif 'F' in atom:
            return 'F'
        elif 'S' in atom:
            return 'S'
        elif 'N' in atom:
            return 'N'
        elif 'O' in atom:
            return 'O'
        elif 'H' in atom:
            return 'H'
        elif 'D' in atom: # deuterium
            return 'D'
        else:
            return atom




