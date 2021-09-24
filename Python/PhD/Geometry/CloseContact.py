
import Geometry.GeoCalcs as calcs
import pandas as pd

class CloseContact:

    def __init__(self,pdb,atomA,atomB,distanceLimit,ridLimit,hue):
        self.pdb = pdb
        self.atomA = atomA
        self.atomB = atomB
        self.distanceLimit = distanceLimit
        self.ridLimit = ridLimit
        self.contacts = []#dictionary of each contact that can be made into a dataframe
        self.dataFrame = None
        self.hue = hue

    def createContacts(self):
        for atmA in self.pdb.atoms:
            atomA = atmA.values['atom']
            if atomA == self.atomA:
                ridA=atmA.values['rid']
                ridxA = atmA.values['ridx']
                aaA = atmA.values['aa']
                chainA = atmA.values['chain']
                occA = atmA.values['occupant']
                atomNoA = atmA.values['atomNo']
                xA = atmA.values['x']
                yA = atmA.values['y']
                zA = atmA.values['z']

                for atmB in self.pdb.atoms:
                    atomB = atmB.values['atom']
                    ridB = atmB.values['rid']
                    ridxB = atmB.values['ridx']
                    aaB = atmB.values['aa']
                    chainB = atmB.values['chain']
                    occB = atmB.values['occupant']
                    atomNoB = atmB.values['atomNo']
                    if atomB == self.atomB and str(ridA)+aaA+chainA+occA != str(ridB)+aaB+chainB+occB:
                        xB = atmB.values['x']
                        yB = atmB.values['y']
                        zB = atmB.values['z']
                        distance = calcs.distance(xA,yA,zA,xB,yB,zB)
                        ridDis = abs(ridA - ridB)

                        if distance <= self.distanceLimit and ridDis >= self.ridLimit:
                            dicOne = {}
                            dicOne['pdbCode'] = self.pdb.pdbCode
                            dicOne['distance'] = float(distance)
                            dicOne['contactA'] = atomA
                            dicOne['aaA'] = aaA
                            dicOne['ridA'] = ridA
                            dicOne['ridxA'] = ridxA
                            dicOne['atomNoA'] = atomNoA
                            dicOne['chainA'] = chainA
                            dicOne['occA'] = occA
                            dicOne['contactB'] = atomB
                            dicOne['aaB'] = aaB
                            dicOne['ridB'] = ridB
                            dicOne['ridxB'] = ridxB
                            dicOne['atomNoB'] = atomNoB
                            dicOne['chainB'] = chainB
                            dicOne['occB'] = occB
                            if self.hue != 'distance':
                                try:
                                    dicOne[self.hue + 'A'] = atmA.values[self.hue]
                                    dicOne[self.hue + 'B'] = atmB.values[self.hue]
                                except:
                                    print('PSU: there is an error with the hue', self.hue)
                            self.contacts.append(dicOne)

        self.dataFrame = pd.DataFrame.from_dict(self.contacts)
        return self.dataFrame

