'''
This class uses the pdb_eda library found here: https://pdb-eda.readthedocs.io/en/latest/index.html
Author: Rachel Alcraft
Date: 01/09/2020
Description:
Loads the matrices via the pdb_eda library and performs a simple normalisaiton (for the future make this configurable)
'''
#import pdb_eda
import numpy as np
import pandas as pd
import math

class GeoDensity:

    def __init__(self,pdbCode,normalisation,pdbDataPath,edDataPath):
        # this defines the data we allow in the atom
        # Structure information
        import pdb_eda
        self.pdbCode = pdbCode
        self.norm = normalisation
        pdb_eda.densityAnalysis.ccp4folder =edDataPath
        pdb_eda.densityAnalysis.pdbfolder = pdbDataPath
        self.analyser = pdb_eda.densityAnalysis.fromPDBid(pdbCode)
        self.factor = 1
        self.translation = 0
        try:
            alpha = self.analyser.densityObj.header.alpha
            self.valid = True
            if self.norm == 'fifty':
                # med = np.median(self.analyser.densityObj.density.ravel())
                minm = self.analyser.densityObj.density.min()
                maxm = self.analyser.densityObj.density.max()
                med = np.median(self.analyser.densityObj.density)
                print('PSU: density min=', minm, 'med=', med, 'max=', maxm)
                # med = np.mean(self.analyser.densityObj.density)

                self.translation = -1 * self.analyser.densityObj.density.min()
                self.factor =  50 / (med + self.translation)
                print('PSU: normalisation trans=',self.translation,'factor=',self.factor)
                print('PSU: normalisation min=', 0, 'med=', (med + self.translation) * self.factor, 'max=', (maxm + self.translation) * self.factor)

            print('PSU: created density for', self.pdbCode)
        except:
            print('PSU: !there is no density for', self.pdbCode)
            self.valid = False

    def getDensityXYZ(self,x,y,z): # this is not the intyerpolated density
        tFoFcx = self.analyser.densityObj.getPointDensityFromXyz([x,y,z])
        tFoFc = self.getInterpolatedDensity(x,y,z,2,-1,'linear',0,0)
        #print(tFoFcx,tFoFc)
        tFoFc += self.translation
        tFoFc *= self.factor
        FoFcx = self.analyser.diffDensityObj.getPointDensityFromXyz([x, y, z])
        FoFc = self.getInterpolatedDensity(x,y,z,1,-1,'linear',0,0)
        #print(FoFcx, FoFc)
        FoFc *= self.factor
        Fo = tFoFc - FoFc
        Fc = tFoFc - 2*FoFc
        return [tFoFc,FoFc,Fo,Fc]

    def getDensityCRS(self,c,r,s): # this is not the intyerpolated density
        tFoFc = self.analyser.densityObj.getPointDensityFromCrs([c,r,s])
        tFoFc += self.translation
        tFoFc *= self.factor
        FoFc = self.analyser.diffDensityObj.getPointDensityFromCrs([c,r,s])
        FoFc *= self.factor
        Fo = tFoFc - FoFc
        Fc = tFoFc - 2*FoFc
        return [tFoFc,FoFc,Fo,Fc]


    def getPeaks(self,allPoints=False,divisor=10):
        if allPoints:
            print("PSU: Warning, the Density points function can take some minutes")
        else:
            print("PSU: Warning, the Density peaks function can take some minutes")
        matrix = self.analyser.densityObj.density
        maxMat = matrix.max()
        if maxMat < 100:
            divisor = 5
        a, b, c = self.analyser.densityObj.density.shape
        print('\t\tPSU: Peaks=',a,'/',end=',')
        finalPeakList = []
        for i in range(0,a):
            peaked = True
            for j in range(0, b):
                peakList = []
                if allPoints:
                    peakList = self.getRowPoints(matrix, i, j, -1,divisor)
                else:
                    peakList = self.getRowPeaks(matrix,i,j,-1)
                for peak in peakList:
                    usePoint = False
                    if allPoints:
                        usePoint = True
                    else:
                        usePoint = self.isPeak(matrix, peak[0], peak[1], peak[2], peak[3], )
                    if usePoint:
                        if peaked:
                            print(peak[0],end=',') # this is just to know it is working as this is very slow
                            peaked = False
                        c,r,s = peak[2],peak[1],peak[0] # the matrix coords seem to be inverted??
                        x,y,z = self.analyser.densityObj.header.crs2xyzCoord([c,r,s]) # convert to x,y,z coordinates to compare with the structure
                        #tfofc, fofc, fo, fc = self.getDensityXYZ(x,y,z)
                        tfofc, fofc, fo, fc = self.getDensityCRS(c,r,s)
                        finalPeakList.append([c,r,s,x,y,z,tfofc,fofc,fo,fc])

        densityData = pd.DataFrame(columns=('pdb_code', 'c', 'r', 's', 'x', 'y', 'z', '2FoFc','FoFc','Fo','Fc'))
        print('', end='\n')
        print('\t\tPSU: Density complete, points=', len(finalPeakList), end='\n')
        for peak in finalPeakList:
            nextrow = len(densityData)
            densityData.loc[nextrow] = (
            self.pdbCode.upper(), peak[0], peak[1], peak[2], peak[3], peak[4], peak[5], peak[6],peak[7],peak[8],peak[9])  # switching ijk to crs


        return (densityData)

    def getRowPeaks(self,matrix,x,y,z):
        '''
        Gets the peaks for a row
        '''
        a,b,c = matrix.shape
        #medMat = np.median(matrix)
        medMat = matrix.max()

        divisor = 8
        if a < 120:
            divisor = 8
        elif a < 150:
            divisor = 8
        elif a < 190:
            divisor = 8

        #print(a,b,c)
        xRange = range(x,x+1)
        yRange = range(y,y+1)
        zRange = range(z,z+1)
        if x == -1:
            xRange = range(0,a)
        if y == -1:
            yRange = range(0,b)
        if z == -1:
            zRange = range(0,c)

        #print(xRange)
        #print(yRange)
        #print(zRange)

        peakList = []
        lastval = -1000
        lastCoordsVal = -1,-1,-1,0
        goingUp = False
        for i in xRange:
            for j in yRange:
                for k in zRange:
                    #print(i,j,k)
                    val = matrix[i,j,k]
                    if val > lastval:
                        goingUp = True
                    else:
                        if goingUp: # then we are now going back down
                            if abs(lastCoordsVal[3]) > medMat/divisor:
                                peakList.append(lastCoordsVal)
                            goingUp = False

                    lastval = val
                    #lastCoordsVal = i,j,k,val
                    lastCoordsVal = i, j, k, val
        return (peakList)

    def getRowPoints(self,matrix,x,y,z,divisor=10):
        '''
        Gets the peaks for a row
        '''
        a,b,c = matrix.shape
        maxMat = matrix.max()
        xRange = range(x,x+1)
        yRange = range(y,y+1)
        zRange = range(z,z+1)
        if x == -1:
            xRange = range(0,a)
        if y == -1:
            yRange = range(0,b)
        if z == -1:
            zRange = range(0,c)
        peakList = []
        for i in xRange:
            for j in yRange:
                for k in zRange:
                    #print(i,j,k)
                    val = matrix[i,j,k]
                    if val >= maxMat/divisor:
                        lastCoordsVal = i, j, k, val
                        peakList.append(lastCoordsVal)
        return (peakList)

    def isPeak(self,matrix,x,y,z,val):
        a, b, c = matrix.shape
        # it is not a peak if all are lower, but same is ok (for now)
        xRange = range(x-1,x+2)
        yRange = range(y-1,y+2)
        zRange = range(z-1,z+2)
        isPeak = True
        for i in xRange:
            for j in yRange:
                for k in zRange:
                    if i>=0 and j>=0 and k>=0:
                        if i<a and j<b and k<c:
                            newval = matrix[i,j,k]
                            if newval > val:
                                isPeak = False


        return (isPeak)

    def getInterpolatedDensity(self, x, y, z, Fo, Fc,interp,differ,degree):
        if interp == 'linear':
            valMain = self.getInterpolatedLinearDensity(x, y, z, False)
            valDiff = self.getInterpolatedLinearDensity(x, y, z, True)
        elif interp in 'spline,splinexyz':
            valMain = self.getInterpolatedSplinedDensity(x, y, z, False,differ,degree,interp)
            valDiff = self.getInterpolatedSplinedDensity(x, y, z, True,differ,degree,interp)
        elif interp == 'sphere':
            valMain = self.getSphereDensity(x, y, z, False)
            valDiff = self.getSphereDensity(x, y, z, True)
        else: # the default is nearest neighbour
            valMain = self.getNeighbourDensity(x, y, z, False)
            valDiff = self.getNeighbourDensity(x, y, z, True)

        valFo = valMain - valDiff
        valFc = valMain - (2*valDiff)
        return (Fo * valFo) + (Fc * valFc)


    def getNeighbourDensity(self,x,y,z,isDiff):
        matrix = self.analyser.densityObj
        if isDiff:
            matrix = self.analyser.diffDensityObj
        noninterp = matrix.getPointDensityFromXyz([x, y, z])
        return noninterp

    def getSphereDensity(self,x,y,z,isDiff):
        matrix = self.analyser.densityObj
        if isDiff:
            matrix = self.analyser.diffDensityObj
        noninterp = matrix.getTotalDensityFromXyz([x,y,z],0.3)
        return noninterp

    def getInterpolatedLinearDensity(self,x,y,z,isDiff):
        noninterp = self.analyser.densityObj.getPointDensityFromXyz([x, y, z])
        nonc,nonr,nons = self.analyser.densityObj.header.xyz2crsCoord([x,y,z])
        nininterpc = self.analyser.densityObj.getPointDensityFromCrs([nonc,nonr,nons])

        matrix = self.analyser.densityObj
        if isDiff:
            matrix = self.analyser.diffDensityObj

        c,r,s = self.Copy_xyz2crsCoord([x,y,z])
        cl,cu = math.floor(c), math.ceil(c)
        rl,ru = math.floor(r), math.ceil(r)
        sl,su = math.floor(s), math.ceil(s)
        points = []
        A = matrix.getPointDensityFromCrs([cl,rl,sl])
        B = matrix.getPointDensityFromCrs([cu,rl,sl])
        C = matrix.getPointDensityFromCrs([cl,rl,su])
        D = matrix.getPointDensityFromCrs([cu,rl,su])
        E = matrix.getPointDensityFromCrs([cl,ru,sl])
        F = matrix.getPointDensityFromCrs([cu,ru,sl])
        G = matrix.getPointDensityFromCrs([cl,ru,su])
        H = matrix.getPointDensityFromCrs([cu,ru,su])

        points.append([[cl,rl,sl,A],[cu,rl,sl,B]])
        points.append([[cl,rl,su,C],[cu,rl,su,D]])
        points.append([[cl,ru,sl,E],[cu,ru,sl,F]])
        points.append([[cl,ru,su,G],[cu,ru,su,H]])

        interps = self.getInterpolatedDensityAndPoints(points,[c,r,s],'linear',None)
        #print(c,r,s)
        #print(interps)
        #print(A,B,C,D,E,F,G,H)

        return interps[3]

    def getInterpolatedSplinedDensity(self,x,y,z,isDiff,differ,degree,interp):
        noninterp = self.analyser.densityObj.getPointDensityFromXyz([x, y, z])
        nonc,nonr,nons = self.analyser.densityObj.header.xyz2crsCoord([x,y,z])
        nininterpc = self.analyser.densityObj.getPointDensityFromCrs([nonc,nonr,nons])

        matrix = self.analyser.densityObj
        if isDiff:
            matrix = self.analyser.diffDensityObj

        co,ro,so = self.Copy_xyz2crsCoord([x,y,z])
        cmax,rmax,smax = matrix.density.shape
        cl,cu = math.floor(co), math.ceil(co)
        rl,ru = math.floor(ro), math.ceil(ro)
        sl,su = math.floor(so), math.ceil(so)
        # allpoints can be generated from cl, rl, sl
        points = []
        xyzpoints = []
        offset = int((degree-1)/2)
        numPoints = 2 + 2*offset
        halfPoints = int(numPoints/2)

        for c in range(cl - offset, cl - offset + numPoints):
            for r in range(rl - offset, rl - offset + numPoints):
                for s in range(sl - offset, sl - offset + numPoints):
                    #don't go out of range
                    #ci,ri,si = max(0,c),max(0, r),max(0, s)
                    #ci,ri,si = min(ci,cmax),min(ri, cmax),min(si, cmax)

                    ci,ri,si=c,r,s #surely this shouldn't work and it should leavge the box?

                    V = matrix.getPointDensityFromCrs([ci, ri, si])
                    points.append([ci,ri,si,V])


        #print('len',len(points))
        interps = self.getSplinedDensityAndPoints(points,[co,ro,so],differ,offset,interp,self.analyser.densityObj.header)
        return interps[3]

    def Copy_xyz2crsCoord(self, xyzCoord):
        """
        Copied from the pdb_eda library and adapted to interpolate
        Convert the xyz coordinates into crs coordinates.
        :param xyzCoord: xyz coordinates.
        :type xyzCoord: A :py:obj:`list` of :py:obj:`float`
        :return: crs coordinates.
        :rtype: A :py:obj:`list` of :py:obj:`int`.
        """
        if self.analyser.densityObj.header.alpha == self.analyser.densityObj.header.beta == self.analyser.densityObj.header.gamma == 90:
            crsGridPos = [(((xyzCoord[i] - self.analyser.densityObj.header.origin[i]) / self.analyser.densityObj.header.gridLength[i])) for i in range(3)]
        else:
            fraction = np.dot(self.analyser.densityObj.header.deOrthoMat, xyzCoord)
            crsGridPos = [((fraction[i] * self.analyser.densityObj.header.xyzInterval[i])) - self.analyser.densityObj.header.crsStart[self.analyser.densityObj.header.map2xyz[i]] for i in range(3)]
        return [crsGridPos[self.analyser.densityObj.header.map2crs[i]] for i in range(3)]

    def getInterpolatedDensityAndPoints(self,points,centre,interp, density_header): #recursive function
        '''
        RECURSIVE
        points is a list of pairs, where each pair is x,y,z followed by the value to interpolate
        List must be 2^x long
        '''
        if len(points) == 1: # end of the recursion, return
            p1 = points[0][0]
            p2 = points[0][1]
            fr = self.getFraction(centre,p1,p2,interp,density_header)
            v = p1[3] + fr * (p2[3] - p1[3])
            x = p1[0] + fr * (p2[0] - p1[0])
            y = p1[1] + fr * (p2[1] - p1[1])
            z = p1[2] + fr * (p2[2] - p1[2])
            return ([x,y,z,v])
        else:#split recursion down further
            half = int(len(points)/2)
            pointsA = points[:half]
            pointsB = points[half:]
            newA = self.getInterpolatedDensityAndPoints(pointsA,centre,interp, density_header)
            newB = self.getInterpolatedDensityAndPoints(pointsB,centre,interp, density_header)
            return self.getInterpolatedDensityAndPoints([[newA,newB]],centre,interp, density_header)

    def getFraction(self, acentre, ap1, ap2, interp, density_header):

        if interp == 'splinexyz': #then the fraction is to be found from the non-ortho=gnal xyz space not the unit square
            #print(acentre,ap1,ap1)
            centre = density_header.crs2xyzCoord([acentre[0],acentre[1],acentre[2]])
            p1 = density_header.crs2xyzCoord([ap1[0], ap1[1], ap1[2]])
            p2 = density_header.crs2xyzCoord([ap2[0], ap2[1], ap2[2]])
            frac = self.getFractionCRSorXYZ(centre, p1, p2)
        else:
            frac = self.getFractionCRSorXYZ(acentre, ap1, ap2)

        return frac

    def getFractionCRSorXYZ(self, centre, p1, p2):
        # The angle beta is found from the cosine rule
        # cos beta  equates x/a to (a^2 + c^2 - b^2) / 2ac
        a = math.sqrt((centre[0] - p1[0]) ** 2 + (centre[1] - p1[1]) ** 2 + (centre[2] - p1[2]) ** 2)
        b = math.sqrt((centre[0] - p2[0]) ** 2 + (centre[1] - p2[1]) ** 2 + (centre[2] - p2[2]) ** 2)
        c = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
        if c == 0:
            fraction = 0
        else:
            x = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
            fraction = x / c
        return (fraction)

    def getSplinedDensityAndPoints(self,points,centre,differ,offset,interp, density_header): #recursive function
        '''
        RECURSIVE
        points is a list of pairs, where each pair is x,y,z followed by the value to interpolate
        List must be 2^x long
        '''
        #print('Recursion depth',len(points))
        numPoints = 2 + offset*2
        #print('len, points', len(points),numPoints)
        if len(points) == numPoints: # end of the recursion, return
            vs = []
            for point in points:
                v = point[3]
                vs.append(v)

            half = int(len(points)/2)
            p1 = points[half-1]
            p2 = points[half]
            fr = self.getFraction(centre,p1,p2,interp, density_header)
            x = p1[0] + fr * (p2[0] - p1[0])
            y = p1[1] + fr * (p2[1] - p1[1])
            z = p1[2] + fr * (p2[2] - p1[2])
            ply = poly.GeoPolynomial(vs,1)
            # the poly is a sequence so the value we want is a fraction along from the halfway markers
            valPoint = half + fr
            finalv = ply.getValue(valPoint,differ)
            return ([x,y,z,finalv])
        else:#split recursion down further
            numPoints = 2+2*offset
            lenPoints = len(points)
            numEach = int(lenPoints/numPoints)
            q1 = int(len(points) / 4)
            half = int(len(points) / 2)
            q3 = half + q1

            #This should be automatic but I can't think how so it is like tis for now:-(
            if numPoints == 2:
                newA = self.getSplinedDensityAndPoints(points[:half], centre, differ,offset,interp, density_header)
                newB = self.getSplinedDensityAndPoints(points[half:], centre, differ,offset,interp, density_header)
                return self.getSplinedDensityAndPoints([newA, newB], centre, differ,offset,interp, density_header)
            elif numPoints == 4:
                newA = self.getSplinedDensityAndPoints(points[:q1], centre, differ,offset,interp, density_header)
                newB = self.getSplinedDensityAndPoints(points[q1:half], centre, differ,offset,interp, density_header)
                newC = self.getSplinedDensityAndPoints(points[half:q3], centre, differ,offset,interp, density_header)
                newD = self.getSplinedDensityAndPoints(points[q3:], centre, differ,offset,interp, density_header)
                return self.getSplinedDensityAndPoints([newA,newB,newC,newD], centre, differ,offset,interp, density_header)
            elif numPoints == 6:
                q1 = int(len(points) * 1 / 6)
                q2 = int(len(points) * 2 / 6)
                q3 = int(len(points) * 3 / 6)
                q4 = int(len(points) * 4 / 6)
                q5 = int(len(points) * 5 / 6)
                #print(len(points), q1, q2, q3, q4, q5)
                newA = self.getSplinedDensityAndPoints(points[:q1], centre, differ,offset,interp, density_header)
                newB = self.getSplinedDensityAndPoints(points[q1:q2], centre, differ,offset,interp, density_header)
                newC = self.getSplinedDensityAndPoints(points[q2:q3], centre, differ,offset,interp, density_header)
                newD = self.getSplinedDensityAndPoints(points[q3:q4], centre, differ,offset,interp, density_header)
                newE = self.getSplinedDensityAndPoints(points[q4:q5], centre, differ,offset,interp, density_header)
                newF = self.getSplinedDensityAndPoints(points[q5:], centre, differ,offset,interp, density_header)
                return self.getSplinedDensityAndPoints([newA,newB,newC,newD,newE,newF], centre, differ,offset,interp, density_header)
            else:
                #print(numPoints,len(points))
                ps = []
                qlast = 0
                for i in range(1,numPoints):
                    qthis = int(len(points) * i/numPoints)
                    newA = self.getSplinedDensityAndPoints(points[qlast:qthis], centre, differ, offset,interp, density_header)
                    ps.append(newA)
                    qlast=qthis
                newA = self.getSplinedDensityAndPoints(points[qlast:], centre, differ, offset,interp, density_header)
                ps.append(newA)
                return self.getSplinedDensityAndPoints(ps, centre, differ, offset,interp, density_header)






