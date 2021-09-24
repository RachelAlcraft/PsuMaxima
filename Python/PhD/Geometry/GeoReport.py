import gc

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Geometry.GeoPlot as geop
import Geometry.GeoPdb as geopdb
import Geometry.CloseContact as geocc

class GeoReport:

    def __init__(self,listPdbs,pdbDataPath,edDataPath,outDataPath,includePdbs=True,ed=True,dssp=True,keepDisordered=True):
        self.pdbDataPath = pdbDataPath
        self.edDataPath = edDataPath
        self.outDataPath = outDataPath
        self.ed = ed
        self.dssp=dssp
        self.keepDisordered = keepDisordered
        self.pdbCodes = listPdbs
        self.plots = []
        self.includePdbs=includePdbs

    def addHistogram(self,geoX='',data=None,title='',ghost=False,operation='',splitKey='',hue='DEFAULT',
                     palette='crimson',count=False,range=[],restrictions={},exclusions={}):
        isNew = False
        if data is None:
            isNew=True
        if hue=='':
            hue='pdbCode'
        gp = geop.GeoPlot(data,geoX,geoY='',title=title,newData=isNew,operation=operation,splitKey=splitKey,
                          plot='histogram',hue=hue,palette=palette,count=count,restrictions=restrictions,exclusions=exclusions,report=self)
        gp.range=range
        if not ghost:
            self.plots.append(gp)
        else:
            self.plots.append(geop.GeoOverlay(gp,'',title='ghost',report=self))

        return gp

    def addStatsCompare(self, dataA=None, dataB=None, descA='',descB='',geoX='', title=''):
        gp = geop.GeoPlot(dataA, geoX, title=title,plot='compare')
        gp.data2 = dataB
        gp.descA = descA
        gp.descB = descB
        self.plots.append(gp)

    def addStatsSummary(self, data=None, desc='',geoX='',geoY='', hue='', title=''):
        gp = geop.GeoPlot(data, geoX, geoY=geoY, title=title,hue=hue,plot='summary')
        gp.descA = desc
        self.plots.append(gp)

    def addScatter(self,geoX='',geoY='',data=None,title='',ghost=False,operation='',splitKey='',hue='bfactor',palette='viridis_r',
                   centre=False,vmin=0,vmax=0,categorical=False,sort='ASC',restrictions={},exclusions={},range=[]):
        isNew = False
        if data is None:
            isNew = True
        if hue == 'dssp':
            categorical=True
        gp = geop.GeoPlot(data, geoX, geoY=geoY, title=title, newData=isNew, operation=operation,splitKey=splitKey,
                          hue=hue,palette=palette,centre=centre,vmin=vmin,vmax=vmax,categorical=categorical,
                          plot='scatter',restrictions=restrictions,exclusions=exclusions,report=self,sort=sort)
        gp.range= range
        if not ghost:
            self.plots.append(gp)
        else:
            self.plots.append(
                geop.GeoOverlay(gp, '', title='ghost', report=self))

    def addHexBins(self,geoX='',geoY='',data=None,title='',gridsize=50,bins=100,ghost=False,operation='',hue='bfactor',palette='viridis_r',restrictions={},exclusions={},range=[]):
        isNew = False
        if data is None:
            isNew = True
        gp = geop.GeoPlot(data, geoX, geoY=geoY, title=title, newData=isNew, operation=operation,
                          hue=hue,palette=palette,plot='hexbin',restrictions=restrictions,exclusions=exclusions,report=self,gridsize=gridsize)

        gp.range = range
        if not ghost:
            self.plots.append(gp)
        else:
            self.plots.append(
                geop.GeoOverlay(gp, '', title='ghost', report=self))

    def addProbability(self,geoX='',geoY='',data=None,title='',ghost=False,operation='',splitKey='',hue='bfactor',palette='viridis_r',centre=False,vmin=0,vmax=0,categorical=False,restrictions={},exclusions={},range=[]):
        isNew = False
        if data is None:
            isNew = True
        gp = geop.GeoPlot(data, geoX, geoY=geoY, title=title, newData=isNew, operation=operation,splitKey=splitKey,
                          hue=hue,palette=palette,centre=centre,vmin=vmin,vmax=vmax,categorical=categorical,
                          plot='probability',restrictions=restrictions,exclusions=exclusions,report=self)
        gp.range = range
        if not ghost:
            self.plots.append(gp)
        else:
            self.plots.append(geop.GeoOverlay(gp, '', title='ghost', report=self))

    def addDifference(self,dataA=None,dataB=None,geoX='',geoY='',restrictionsA={},restrictionsB = {},exclusionsA={},exclusionsB={},title='',palette='seismic'):
        isNew = False
        if dataA is None:
            isNew = True
        diffPlot = geop.GeoDifference(dataA=dataA,dataB=dataB,geoX=geoX,geoY=geoY,title=title,
                                      palette=palette,restrictionsA=restrictionsA,restrictionsB=restrictionsB,
                                      exclusionsA=exclusionsA,exclusionsB=exclusionsB,newData=isNew,report=self)

        self.plots.append(diffPlot.plotA)
        self.plots.append(diffPlot.plotDiff)
        self.plots.append(diffPlot.plotB)

    def addCloseContact(self,pdbCode,atomA,atomB,distanceLimit=8.0,ridLimit=2,palette='viridis',hue='distance',categorical=False,title=''):
        pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
        pdb = pdbmanager.getPdb(pdbCode,True)
        cc = geocc.CloseContact(pdb,atomA,atomB,distanceLimit,ridLimit,hue)
        if hue !='distance':
            hue = hue+'A'
        df = cc.createContacts()
        if title != '':
            title += '\n'
        title +=atomA+':'+atomB + '\n'
        title += 'Max Contact=' +  str(distanceLimit) + 'Å\n'
        title += 'Residue Gap=' + str(ridLimit)
        gp = geop.GeoPlot(data=df, geoX='ridxA', geoY='ridxB', title=title, newData=False, hue=hue,
                          palette=palette, plot='contact',categorical=categorical,report=self)
        self.plots.append(gp)
        return df


    def addCsv(self, data, title=''):
        gp = geop.GeoPlot(data=data,title=title,plot='csv',geoX='')
        self.plots.append(gp)

    def addComment(self, comment):
        gp = geop.GeoPlot(data=pd.DataFrame(),title=comment,plot='comment',geoX='')
        self.plots.append(gp)

    def addDataView(self, pdbCode, geoX, geoY, palette='viridis', hue='2FoFc', categorical=False, title='',centre=False,sort='ASC'):
        pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
        apdb = pdbmanager.getPdb(pdbCode,True)
        df = apdb.getDataFrame()
        self.addScatter(data=df, geoX=geoX, geoY=geoY, title=title, hue=hue, palette=palette,categorical=categorical,centre=centre,sort=sort)

    def addDensityView(self, pdbCode, geoX, geoY, peaks=True,divisor=10, palette='viridis', hue='2FoFc', categorical=False, title=''):
        pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
        apdb = pdbmanager.getPdb(pdbCode,True)
        allPoints = not peaks
        if apdb.hasDensity:
            peaksData = apdb.getStructureDensity(allPoints,divisor,self.pdbDataPath,self.edDataPath)
            self.addScatter(data=peaksData, geoX=geoX, geoY=geoY, title=title, hue=hue, palette=palette,categorical=categorical)

    def addSurfaceOverlay(self, surfaces, title='',logged=False):
        mat = []
        gp = geop.GeoPlot(data=None, geoX='', title=title, plot='surfaces', report=self)
        gp.surface = surfaces
        gp.logged=logged
        self.plots.append(gp)
        return mat


    def getGeoemtryCsv(self,calcList, hueList,bfactorFactor=-1,allAtoms=False,restrictedAa = 'ALL'):
        dfs = []
        pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp,self.keepDisordered)
        count = 0
        for pdb in self.pdbCodes:
            count = count + 1
            if not pdbmanager.existsPdb(pdb):
                print('PSU: get',pdb,count,'/',len(self.pdbCodes))
            apdb = pdbmanager.getPdb(pdb,allAtoms)
            data = apdb.getGeoemtryCsv(calcList, hueList,bfactorFactor,restrictedAa)
            dfs.append(data)
        if len(dfs) > 0:
            df = pd.concat(dfs, ignore_index=True)
            return (df)
        else:
            return pd.DataFrame.empty

    def getReportCsv(self, reportName):
        hueList = ['2FoFc','FoFc','bfactor','aa','dssp']
        if reportName == 'Ramachandran':
            calcList = ['C-1:N:CA:C', 'N:CA:C:N+1']
        elif reportName == 'Sp2Planarity':
            calcList = ['CA:C:O','O:C:N+1','N+1:C:CA','N+1:O:C:CA']
        elif reportName == 'Sp3Tetrahedra':
            calcList = ['N:CA:C','C:CA:CB','N:CA:CB']
        elif reportName == 'BackboneOutliers':
            calcList = ['C-1:N','N:CA','CA:C','C:N+1','C-1:N:CA','N:CA:C','CA:C:N+1']
        elif reportName == 'MainChainHistograms':
            calcList = ['C-1:N','N:CA','CA:C','C:N+1','C-1:N:CA','N:CA:C','CA:C:N+1','C:O','CA-1:CA','CA:CA+1','CA:C:N+1:CA+1','C-1:N:CA:C','N:CA:C:N+1']
        elif reportName == 'OmegaCis':
            calcList = ['CA-1:CA','CA:CA+1','CA:C:N+1:CA+1','CA-1:C-1:N:CA','N:CA:C']
        elif reportName == 'RachelsChoice' or reportName == 'RachelsChoiceNonXRay':
            calcList = ['N:O','CB:O','N:CA:C:N+1','C-1:N:CA:C']
        df = self.getGeoemtryCsv(calcList,hueList)
        return (df)


    def printReport(self, reportName,fileName):
        print('PSU: create report',reportName,'for',fileName)
        self.flush()

        printList = []
        if reportName == 'BackboneOutliers': # Sp2Planarity, DensityAtomCompare, OmegaCis
            atomData = self.getReportCsv(reportName)
            title = 'Backbone Outliers Report'
            cols = 3
            printList = []
            #printList.append(GeoQuery(['Bonds', atomData, 'C-1:N', 'N:CA','aa', '2FoFc', 'viridis_r', False, 0, 0])
            self.addScatter(data=atomData,geoX='C-1:N',geoY='N:CA',title='Bonds',ghost=True)
            self.addScatter(data=atomData, geoX='CA:C', geoY='C:N+1', title='Bonds',ghost=True)
            self.addScatter(data=atomData, geoX='C-1:N', geoY='C:N+1', title='Bonds',ghost=True)
            self.addScatter(data=atomData, geoX='C-1:N:CA', geoY='N:CA:C', title='Angles',ghost=True)
            self.addScatter(data=atomData, geoX='N:CA:C', geoY='CA:C:N+1', title='Angles',ghost=True)
            self.addScatter(data=atomData, geoX='C-1:N:CA', geoY='CA:C:N+1', title='Angles',ghost=True)
            self.printToHtml(title, cols, fileName)
        elif reportName == 'RachelsChoice' or reportName == 'RachelsChoiceNonXRay' :
            atomData = self.getReportCsv(reportName)
            # We want the dummy trace correlation plot so we can see if there are areas of interest
            title = "Rachel's Choice of Correlations"
            cols = 4
            printList = []

            densityHue = '2FoFc'
            if reportName == 'RachelsChoiceNonXRay':
                densityHue = 'bfactor'

            self.addScatter(geoX='C-1:N:CA:C', geoY='N:CA:C:N+1', title='', hue='dssp',palette='gist_rainbow',ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='N:CA:C:N+1', title='', hue=densityHue, palette='cubehelix_r',ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='N:CA:C:N+1', title='', hue='aa', palette='gist_rainbow',ghost=True,categorical=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='N:CA:C:N+1', title='', hue='pdbCode', palette='gist_rainbow',ghost=True,categorical=True)

            self.addScatter(geoX='N:CA:CB:CG', geoY='CA:CB:CG:CD', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:CA:CB:CG', geoY='CA:CB:CG:CD', title='', hue=densityHue, palette='cubehelix_r',ghost=True)
            self.addScatter(geoX='N:CA:CB:CG', geoY='CA:CB:CG:CD', title='', hue='aa', palette='gist_rainbow',ghost=True,categorical=True)
            self.addScatter(geoX='N:CA:CB:CG', geoY='CA:CB:CG:CD', title='', hue='pdbCode', palette='gist_rainbow',ghost=True,categorical=True)

            self.addScatter(geoX='N:CA', geoY='CA:C', title='', hue='dssp', palette='gist_rainbow',ghost=True)
            self.addScatter(geoX='N:CA', geoY='CA:C', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='N:CA', geoY='CA:C', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='N:CA', geoY='CA:C', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='CA:CA+1', geoY='CA-1:CA', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='CA:CA+1', geoY='CA-1:CA', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='CA:CA+1', geoY='CA-1:CA', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='CA:CA+1', geoY='CA-1:CA', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='N:CA:C', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='N:CA:C', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='N:CA:C', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='N:CA:C', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='N:O', geoY='CB:O', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:O', geoY='CB:O', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='N:O', geoY='CB:O', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='N:O', geoY='CB:O', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='N:CA:C:N+1', geoY='N:O', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:O', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:O', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:O', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='N:CA:C:N+1', geoY='CB:O', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CB:O', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CB:O', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CB:O', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='N:CA:C:N+1', geoY='N:CA:C:O', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:CA:C:O', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:CA:C:O', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='N:CA:C:O', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='N:CA:C:N+1', geoY='CA-1:CA:CA+1', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CA-1:CA:CA+1', title='', hue=densityHue, palette='cubehelix_r',ghost=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CA-1:CA:CA+1', title='', hue='aa', palette='gist_rainbow',ghost=True,categorical=True)
            self.addScatter(geoX='N:CA:C:N+1', geoY='CA-1:CA:CA+1', title='', hue='pdbCode', palette='gist_rainbow',ghost=True,categorical=True)

            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:C', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:C', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:C', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:C', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:CB', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:CB', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:CB', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='C-1:N:CA:C', geoY='C-1:CB', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='CA-1:C-1:N:CA', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='CA-1:C-1:N:CA', title='', hue=densityHue, palette='cubehelix_r',ghost=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='CA-1:C-1:N:CA', title='', hue='aa', palette='gist_rainbow',ghost=True,categorical=True)
            self.addScatter(geoX='CA:C:N+1:CA+1', geoY='CA-1:C-1:N:CA', title='', hue='pdbCode', palette='gist_rainbow',ghost=True,categorical=True)

            self.addScatter(geoX='CA-2:CA-1:CA', geoY='CA:CA+1:CA+2', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='CA-2:CA-1:CA', geoY='CA:CA+1:CA+2', title='', hue=densityHue, palette='cubehelix_r',ghost=True)
            self.addScatter(geoX='CA-2:CA-1:CA', geoY='CA:CA+1:CA+2', title='', hue='aa', palette='gist_rainbow',ghost=True,categorical=True)
            self.addScatter(geoX='CA-2:CA-1:CA', geoY='CA:CA+1:CA+2', title='', hue='pdbCode', palette='gist_rainbow',ghost=True,categorical=True)

            self.addScatter(geoX='C-1:N:CA', geoY='CA:C:N+1', title='', hue='dssp', palette='gist_rainbow', ghost=True)
            self.addScatter(geoX='C-1:N:CA', geoY='CA:C:N+1', title='', hue=densityHue, palette='cubehelix_r', ghost=True)
            self.addScatter(geoX='C-1:N:CA', geoY='CA:C:N+1', title='', hue='aa', palette='gist_rainbow', ghost=True,categorical=True)
            self.addScatter(geoX='C-1:N:CA', geoY='CA:C:N+1', title='', hue='pdbCode', palette='gist_rainbow', ghost=True,categorical=True)

            self.printToHtml(title, cols, fileName)

        elif reportName == 'MainChainHistograms': # Sp2Planarity, DensityAtomCompare, OmegaCis
            atomData = self.getReportCsv(reportName)
            title = 'Main Chain Histograms'
            cols = 3
            printList = []

            self.addHistogram(data=atomData,geoX='C-1:N',title='C-1:N',hue='rid',ghost=True)
            self.addHistogram(data=atomData,geoX='N:CA',title='O:C:N+1',hue='rid',ghost=True)
            self.addHistogram(data=atomData,geoX='CA:C',title='N+1:C:CA',hue='rid',ghost=True)

            self.addHistogram(data=atomData, geoX='C:O', title='C:0', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='CA-1:CA', title='CA-1:CA', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='CA:CA+1', title='CA:CA+1', hue='rid',ghost=True)

            self.addHistogram(data=atomData, geoX='C-1:N:CA', title='Tau-1', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='N:CA:C', title='Tau', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='CA:C:N+1', title='Tau+1', hue='rid',ghost=True)

            self.addHistogram(data=atomData, geoX='C-1:N:CA:C', title='PHI', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='N:CA:C:N+1', title='PSI', hue='rid',ghost=True)
            self.addHistogram(data=atomData, geoX='CA:C:N+1:CA+1', title='AbsVal OMEGA', hue='rid', operation='ABS',ghost=True)

            self.printToHtml(title, cols, fileName)

        elif reportName == 'Sp2Planarity': # Sp2Planarity, DensityAtomCompare, OmegaCis
            atomData = self.getReportCsv(reportName)
            title = 'Sp2 Planarity'
            cols = 4
            printList = []
            self.addHistogram(data=atomData,geoX='N+1:O:C:CA',title='AbsVal Dihedral',hue='rid',operation='ABS')
            self.addHistogram(data=atomData,geoX='CA:C:O',title='CA:C:O',hue='rid')
            self.addHistogram(data=atomData,geoX='O:C:N+1',title='O:C:N+1',hue='rid')
            self.addHistogram(data=atomData,geoX='N+1:C:CA',title='N+1:C:CA',hue='rid')

            self.addScatter(data=atomData, geoX='N+1:O:C:CA', geoY='CA:C:O',hue='dssp')
            self.addScatter(data=atomData, geoX='N+1:O:C:CA', geoY='O:C:N+1')
            self.addScatter(data=atomData, geoX='N+1:O:C:CA', geoY='N+1:C:CA',hue='bfactor')
            self.addScatter(data=atomData, geoX='N+1:C:CA', geoY='O:C:N+1',hue='FoFc', palette='Spectral',centre=True)

            self.printToHtml(title, cols, fileName)

        elif reportName == 'DataPerPdb':
            pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
            for pdb in self.pdbCodes:
                print('\tPSU:', reportName, 'for', pdb)
                apdb = pdbmanager.getPdb(pdb,True)
                atomData = apdb.getDataFrame()
                title = 'General Data Report'
                cols = 3
                self.addScatter(data=atomData, geoX='atomNo', geoY='aa', hue='aa', categorical=True,palette='gist_rainbow')
                self.addScatter(data=atomData, geoX='atomNo', geoY='dssp',hue= 'aa',categorical=True,palette='gist_rainbow')
                self.addScatter(data=atomData, geoX='2FoFc', geoY='bfactor',hue= 'element',palette='jet_r',categorical=True)
                self.addScatter(data=atomData, geoX='atomNo', geoY='bfactor',hue= 'element',palette='jet_r',categorical=True)
                self.addScatter(data=atomData, geoX='atomNo', geoY='2FoFc',hue='element',palette='jet_r',categorical=True)
                self.addScatter(data=atomData, geoX='atomNo', geoY='FoFc',hue='element',palette='jet_r',categorical=True)
                self.addScatter(data=atomData, geoX='x', geoY='y',hue='atomNo', palette='plasma_r')
                self.addScatter(data=atomData, geoX='y', geoY='z',hue='atomNo', palette='plasma_r')
                self.addScatter(data=atomData, geoX='z', geoY='x',hue='atomNo', palette='plasma_r')
                self.printToHtml(title, cols, fileName + '_' + apdb.pdbCode)

        elif reportName == 'Slow_DensityPointsPerPdb' or reportName == 'Slow_DensityPeaksPerPdb': # this can only be done per pdb
            for pdb in self.pdbCodes:
                pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
                apdb = pdbmanager.getPdb(pdb,True)
                if apdb.hasDensity:
                    print('\tPSU:', reportName, 'for', apdb.pdbCode)
                    allPoints = True
                    maintitle = 'Density Points and Atoms Comparison'
                    if reportName == 'Slow_DensityPeaksPerPdb':
                        allPoints = False
                        maintitle = 'Density Peaks and Atoms Comparison'
                    peaksData = apdb.getStructureDensity(allPoints,10,self.pdbDataPath,self.edDataPath)
                    atomData = apdb.getDataFrame()
                    atomData['FoFc2'] = atomData['FoFc'] ** 2

                    cols = 3
                    printList = []
                    self.addScatter(data=peaksData, geoX='c', geoY='r', title='Density CR Fo',hue='Fo',palette='gist_gray_r')
                    self.addScatter(data=peaksData, geoX='r', geoY='s',title='Density RS Fo',hue='Fo',palette='gist_gray_r')
                    self.addScatter(data=peaksData, geoX='s', geoY='c',title='Density SC Fo',hue='Fo',palette='gist_gray_r')

                    self.addScatter(data=peaksData, geoX='c', geoY='r',title='Density CR Fo',hue='Fo',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='r', geoY='s',title='Density RS Fo',hue='Fo',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='s', geoY='c',title='Density SC Fo',hue='Fo',palette='cubehelix_r')

                    self.addScatter(data=peaksData, geoX='c', geoY='r',title='Density CR 2FoFC',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='r', geoY='s',title='Density RS 2FoFC',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='s', geoY='c',title='Density SC 2FoFC',hue='2FoFc',palette='cubehelix_r')

                    self.addScatter(data=peaksData, geoX='c', geoY='r',title='Density CR FC',hue='Fc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='r', geoY='s',title='Density RS FC',hue='Fc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='s', geoY='c',title='Density SC FC',hue='Fc',palette='cubehelix_r')

                    self.addScatter(data=peaksData, geoX='c', geoY='r',title='Density CR FoFC',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=peaksData, geoX='r', geoY='s',title='Density RS FoFC',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=peaksData, geoX='s', geoY='c',title='Density SC FoFC',hue='FoFc',palette='PiYG',centre=True)

                    self.addScatter(data=peaksData, geoX='x', geoY='y',title='Density XY Fo',hue='Fo',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='y', geoY='z',title='Density YZ Fo',hue='Fo',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='z', geoY='x',title='Density ZX Fo',hue='Fo',palette='cubehelix_r')

                    self.addScatter(data=peaksData, geoX='x', geoY='y',title='Density XY FoFC',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=peaksData, geoX='y', geoY='z',title='Density YZ FoFC',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=peaksData, geoX='z', geoY='x', title='Density ZX FoFC',hue='FoFc',palette='PiYG',centre=True)

                    self.addScatter(data=peaksData, geoX='x', geoY='y',title='Density XY 2FoFC',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='y', geoY='z',title='Density YZ 2FoFC',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=peaksData, geoX='z', geoY='x',title='Density ZX 2FoFC',hue='2FoFc',palette='cubehelix_r')

                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY 2FoFc',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ 2FoFc',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX 2FoFc',hue='2FoFc',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY Electrons',hue='electrons',palette='Spectral_r',categorical=True)
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ Electrons',hue='electrons',palette='Spectral_r',categorical=True)
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX Electrons',hue='electrons',palette='Spectral_r',categorical=True)
                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY FoFc',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ FoFc',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX FoFc',hue='FoFc',palette='PiYG',centre=True)
                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY bfactor',hue='bfactor',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ bfactor',hue='bfactor',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX bfactor',hue='bfactor',palette='cubehelix_r')
                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY atom nos',hue='atomNo',palette='gist_ncar')
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ atom nos',hue='atomNo',palette='gist_ncar')
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX atom nos',hue='atomNo',palette='gist_ncar')
                    self.addScatter(data=atomData, geoX='x', geoY='y',title='PDB XY amino acids',hue='aa',palette='nipy_spectral',categorical=True)
                    self.addScatter(data=atomData, geoX='y', geoY='z',title='PDB YZ amino acids',hue='aa',palette='nipy_spectral',categorical=True)
                    self.addScatter(data=atomData, geoX='z', geoY='x',title='PDB ZX amino acids',hue='aa',palette='nipy_spectral',categorical=True)
                    self.addScatter(data=atomData, geoX='bfactor', geoY='2FoFc',title='PDB bfactor vs 2FoFc',hue='electrons',palette='viridis_r',categorical=True)
                    self.addScatter(data=atomData, geoX='Fc', geoY='Fo',title='PDB Fc vs Fc',hue='electrons',palette='viridis_r',categorical=True)
                    self.addScatter(data=atomData, geoX='electrons', geoY='2FoFc',title='PDB electrons vs 2FoFc',hue='element',palette='viridis_r',categorical=True)
                    self.addHistogram(data=atomData, geoX='aa',title='Amino Acids')
                    self.addHistogram(data=atomData, geoX='element',title='Atoms')
                    self.addHistogram(data=atomData, geoX='2FoFc',title='Peaks in 2FoFc')
                    self.printToHtml(maintitle, cols, fileName + '_' + apdb.pdbCode)
                else:
                    print('\tPSU:',apdb.pdbCode,'has no density matrix')




    #def printCsvToHtml(self, queryList,pdbList,title,cols,printPath,fileName):
    def printToHtml(self, maintitle, cols, fileName):
        print('PSU: formatting to html...')
        width=str(100/cols)
        reportPath = self.outDataPath + fileName + ".html"
        count = 0
        #html += '<table style="width:90%">\n'
        html = '<table>\n'
        row = 1
        for geoPl in self.plots:
            #fig, ax = plt.subplots()
            if type(geoPl) is geop.GeoPlot and geoPl.plot != 'csv' and geoPl.plot != 'comment':
                #html += self.twoPlots(geoPl.plotA,geoPl.plotB,width)

                title = geoPl.title
                alldata = geoPl.data
                geoX = geoPl.geoX
                geoY = geoPl.geoY
                splitKey = geoPl.splitKey
                splitList = ['']
                if splitKey != '':
                    splitList = alldata[splitKey].unique()
            else:
                splitList = ['']


            if True:

                for split in splitList:
                    geoqSplit = geoPl
                    if count == 0:
                        html += '<tr><td colspan=' + '"' + str(cols) + '"' + '>Row ' + str(row) + '</td></tr>\n'
                        row += 1
                        html += '<tr>'
                    elif count % cols == 0:
                        html += '</tr>\n'
                        html += '<tr><td colspan=' + '"' + str(cols) + '"' + '>Row ' + str(row) + '</td></tr>\n'
                        row += 1
                        html += '<tr>'


                    count += 1

                    if split != '':
                        data = alldata[alldata[splitKey] == split]
                        geoqSplit.data = data
                        geoqSplit.title = title + ' ' + split

                    print('PSU: plot',count,'/',len(self.plots))
                    if type(geoqSplit) is geop.GeoOverlay:
                        html += self.twoPlotsOverlay(geoPl.plotA,geoPl.plotB,width)
                    elif type(geoqSplit) is geop.GeoDifference:
                        html += self.onePlot(geoqSplit, width)
                    else:
                        html += self.onePlot(geoqSplit, width)

        html += '</tr></table>'
                #'<hr/><p>Produced by PsuGeometry, written by Rachel Alcraft<br/>Please cite the application note...</p></body>\n'

        if fileName == "STRING":
            return html #without the header and the footer
        else:
            html += '<hr/><p style = "background-color:tomato;" >'
            html += '<a href = "https://rachelalcraft.github.io/psugeometry.html" title = "PsuGeometry" target = "_self">PsuGeometry</a>'
            html += ' by <a href = "mailto:rachelalcraft@gmail.com">Rachel Alcraft</a>'
            html += '. Follow <a href = "https://rachelalcraft.github.io/citing.html"> citation guidance </a> </br></p><hr/>'

            hhtml = self.getHeaderString(fileName, maintitle)
            # and print
            f = open(reportPath, "w+")
            f.write(hhtml + html)
            print('PSU: saved file to',reportPath)
            self.flush()
            f.close()

    def getHeaderString(self,fileName,title):
        html = '<!DOCTYPE html><html lang="en"><head><title>PSU-' + fileName + '-GEO</title>\n'
        # html += '<style> body {background-color:SeaShell;} table {table-layout:fixed;display:table;margin:0 auto;}td {border:1px solid RosyBrown;background-color:SeaShell;}</style>'
        # html += '<style> body {background-color:HoneyDew;} table {background-color:HoneyDew;} .innertable td {border:1px solid MistyRose;background-color:MintCream;}</style>'
        html += '<style> body {text-align:center;background-color:LightSteelBlue ;} img {width:95% }'
        html += 'table {font-size:0.8vw;width:95%;table-layout:fixed;display:table;margin:0 auto;background-color:LightSteelBlue ;}'
        html += ' td {border:1px solid MistyRose;background-color:AliceBlue;}</style>'
        html += '</head>\n'
        html += '<body><h1>' + title + '</h1>\n'
        html += '<h2>PSU: Geometric Correlations</h2>\n'
        html += '<hr/>'

        pdbmanager = geopdb.GeoPdbs(self.pdbDataPath, self.edDataPath, self.ed, self.dssp)
        if len(self.pdbCodes) > 0 and self.includePdbs == True:
            html += '<table><tr><td>PdbCode</td><td>Resolution</td><td>Pdb Link</td><td>PDBe Link</td></tr>\n'
            for pdb in self.pdbCodes:
                html += '<tr>\n'
                html += '<td>' + pdb + '</td>\n'
                res = ''
                if pdbmanager.existsPdb(pdb):
                    apdb = pdbmanager.getPdb(pdb,False)
                    res = str(apdb.atoms[0].values['resolution'])
                html += '<td>' + res + '</td>\n'
                html += "<td><a href='https://www.rcsb.org/structure/" + pdb + "' title='PDB Link' target='_blank'>Link to PDB</a></td>\n"
                html += "<td><a href='https://www.ebi.ac.uk/pdbe/entry/pdb/" + pdb + "' title='PDB Link' target='_blank'>Link to PDBe</a></td>\n"
                html += '</tr>\n'
            html += '</table>\n'
            html += '</table>\n'

        html += '<hr/>\n'
        return html

    def onePlot(self,geoPl, width):
        #matplotlib.use('Agg')
        #plt.ioff()
        #try:
        if True:
            if geoPl.newData:
                geoPl.getNewData()

            geoPl.applyRestrictions()
            geoPl.applyExclusions()

            #plt.close('all')
            #gc.collect()

            if geoPl.plot=='surface' or geoPl.plot=='surfaces':
                fig, ax = plt.subplots()
                ret = geoPl.plotToAxes(fig,ax)
                encoded = geoPl.getPlotImage(fig,ax)
                htmlstring = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
                htmlstring += ret
                html = '<td width=' + width + '%><p>' + geoPl.title + '</p>\n<p>' + htmlstring + '</p></td>\n'
            elif geoPl.plot == 'comment':  # Just a single comment
                html = '<td width=' + width + '%>' + '<p>' + geoPl.title + '</p></td>\n'
            elif geoPl.hasMatrix:
                fig, ax = plt.subplots()
                ret = geoPl.plotToAxes(fig,ax)
                encoded = geoPl.getPlotImage(fig,ax)
                htmlstring = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
                htmlstring += ret
                html = '<td width=' + width + '%>' + '<p>' + htmlstring + '</p></td>\n'
                #fig.clear()
                plt.close('all')
            elif geoPl.data.empty:
                html = '<td width=' + width + '%>' + 'No Data:' + geoPl.geoX + ' ' + geoPl.geoY  + '</td>\n'
            elif geoPl.plot == 'compare':#there is no plot
                fig, ax = plt.subplots()
                ret = geoPl.plotToAxes(fig,ax)
                htmlstring = ret
                html = '<td width=' + width + '%>' + '<p>' + htmlstring + '</p></td>\n'
            elif geoPl.plot == 'summary' or geoPl.plot == 'csv' or geoPl.plot=='comment':#there is no plot
                ret = geoPl.plotNoAxes()
                htmlstring = ret
                html = '<td width=' + width + '%>' + '<p>' + htmlstring + '</p></td>\n'
            else:
                fig, ax = plt.subplots()
                ret = geoPl.plotToAxes(fig,ax)
                encoded = geoPl.getPlotImage(fig,ax)
                htmlstring = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
                htmlstring += ret
                html = '<td width=' + width + '%>' + '<p>' + htmlstring + '</p></td>\n'
        #except:
        #    html = '<td width=' + width + '%>' + 'Error:' + geoPl.geoX + ' ' + geoPl.geoY + '</td>\n'


        plt.close('all')
        #gc.collect()
        return (html)


    def twoPlotsOverlay(self,geoPlA,geoPlB,width):
        '''
        https://stackoverflow.com/questions/6871201/plot-two-histograms-on-single-chart-with-matplotlib
        '''
        #try:
        if True:
            fig, ax = plt.subplots()
            if geoPlA.newData:
                geoPlA.getNewData()
            if geoPlB.newData:
                geoPlB.getNewData()

            geoPlA.applyRestrictions()
            geoPlA.applyRestrictions()
            geoPlA.applyExclusions()
            geoPlB.applyRestrictions()
            geoPlB.applyExclusions()

            if geoPlA.plot == 'probabilty':
                retA = geoPlB.plotToAxes(fig, ax) # for probability plot ghost second as it is alpha 0.5 over the top
                retB = geoPlA.plotToAxes(fig, ax)
            else:
                retA = geoPlA.plotToAxes(fig, ax)
                retB = geoPlB.plotToAxes(fig, ax)
            encoded = geoPlA.getPlotImage(fig, ax)

            htmlstring = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')) + '\n'
            htmlstring += retA + retB

            if geoPlA.data.empty:
                html = '<td width=' + width + '%>' + 'No Data:' + geoPlA.geoX + ' ' + geoPlA.geoY  + '</td>\n'
            else:
                html = '<td width=' + width + '%>' + htmlstring + '</td>\n'
        #except:
        #    html = '<td width=' + width + '%>' + 'Error:' + geoPlA.geoX + ' ' + geoPlA.geoY + '</td>\n'

        return (html)


    def addSlices(self, slices, palette='viridis', title='',logged=False,centre=False,Contour=True):
        mat = []
        for s in slices:
            if mat == []:
                mat = s
            else:
                mat = mat + s
        gp = geop.GeoPlot(data=None, geoX='', title=title, palette=palette, plot='surface', report=self,centre=centre,Contour=Contour)
        gp.surface = mat
        gp.logged=logged
        self.plots.append(gp)
        return mat

    def addSlice(self, slice, palette='viridis', title='',logged=False,centre=False,Contour=True,YellowDots=np.array([])):
        gp = geop.GeoPlot(data=None,geoX='',title=title, palette=palette, plot='surface', report=self,centre=centre,Contour=Contour)
        gp.surface = slice
        gp.logged=logged
        gp.differ=0
        gp.YellowDots = YellowDots
        self.plots.append(gp)

    def saveSlice(self,dataarray, filepath):
        with open(filepath, 'w') as outfile:
            x, y = dataarray.shape
            for i in range(0,x):
                for j in range(0, y):
                    val = dataarray[i,j]
                    if j > 0:
                        outfile.write(str(','))
                    elif i > 0:
                        outfile.write(str('\n'))
                    outfile.write(str(val))

    def loadSlice(self,filepath):

        with open(filepath,'r') as f:
            ed_data = f.read().splitlines()

        rows = len(ed_data)
        ed_slice = np.zeros((rows,rows))
        for i in range(0,rows):
            row = ed_data[i].split(',')
            for j in range(0, rows):
                val = float(row[j])
                ed_slice[i,j] = val

        return ed_slice


    def flush(self):
        self.plots = []
        html = ''
        self.dataFrame = None

