

/************************************************************************
* RSA 10.9.21
************************************************************************/

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

#include "VectorThree.h"
#include "SpaceTransformation.h"

#include "CoutReports.h"

using namespace std;


void CoutReports::coutPeaks(Ccp4* ccp4, PdbFile* pdb)
{
    sort(ccp4->MatrixPeaks.rbegin(), ccp4->MatrixPeaks.rend());
    vector<pair<float, int> > tmpMatrixPeaks;

    //All the data in the list is near neighbours. So we can go through it
    //TO DO HERE
    for (unsigned int i = 0;  i< ccp4->MatrixPeaks.size(); ++i)
    {
        double peak = ccp4->MatrixPeaks[i].first;
        int position = ccp4->MatrixPeaks[i].second;
        VectorThree CRS = ccp4->getCRS(position);
        bool are_any_bigger = false;
        for (int a = -1; a < 2; ++ a)
        {
            for (int b = -1; b < 2; ++ b)
            {
                for (int c = -1; c < 2; ++ c)
                {                    
                    int tmpPos = ccp4->getPosition(a + CRS.A, b + CRS.B, c + CRS.C);
                    if (tmpPos > 0 && tmpPos < ccp4->Matrix.size())
                    {
                        double tmpPeak = ccp4->Matrix[tmpPos];
                        if (tmpPeak > peak)
                            are_any_bigger = true;
                    }
            
                }            
            }
        }
        if (!are_any_bigger)
        {
            tmpMatrixPeaks.push_back(pair<float,int>(peak,position));
        }

    }

    ccp4->MatrixPeaks = tmpMatrixPeaks;

    unsigned int maxdensity = 10000;
    if (ccp4->MatrixPeaks.size() < maxdensity)
        maxdensity = ccp4->MatrixPeaks.size();

    

    cout << "BEGIN_ALLPEAKS\n";
    cout << "Density,C,R,S,X,Y,Z,NearestAtom,Distance\n";


    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        int pos = ccp4->MatrixPeaks[i].second;
        VectorThree coords = ccp4->getCRS(pos);
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.C, coords.B, coords.A);
        float density = ccp4->MatrixPeaks[i].first;
        double distance = 0;
        string line = "-";
        if (pdb->isLoaded())
        {
            Atom* atm = pdb->getNearest(XYZ.A, XYZ.B, XYZ.C);
            if (atm != NULL)
            {
                line = atm->getLine();
                distance = atm->distance(XYZ.A, XYZ.B, XYZ.C);
            }
        }
        if (line == "-")
            cout << "" << density << "," << coords.C << "," << coords.B << "," << coords.A << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << line << ",-" << "\n";
        else
            cout << "" << density << "," << coords.C << "," << coords.B << "," << coords.A << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << line << "," << distance << "\n";
    }
    cout << "END_ALLPEAKS\n";

    cout << "BEGIN_ATOMPEAKS\n";
    cout << "Density,C,R,S,X,Y,Z,NearestAtom,Distance\n";
    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        int pos = ccp4->MatrixPeaks[i].second;
        VectorThree coords = ccp4->getCRS(pos);
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.C, coords.B, coords.A);
        float density = ccp4->MatrixPeaks[i].first;
        double distance = 0;
        string line = "-";
        if (pdb->isLoaded())
        {
            Atom* atm = pdb->getNearest(XYZ.A, XYZ.B, XYZ.C);
            if (atm != NULL)
            {
                line = atm->getLine();
                distance = atm->distance(XYZ.A, XYZ.B, XYZ.C);
            }
        }
        if (line != "-")                    
            cout << "" << density << "," << coords.C << "," << coords.B << "," << coords.A << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << line << "," << distance << "\n";
    }
    cout << "END_ATOMPEAKS\n";

}

void CoutReports::coutAtoms(Ccp4* ccp4, PdbFile* pdb)
{
    cout << "BEGIN_ATOMDENSITY\n";
    cout << "Density,X,Y,Z,AtomNo,AtomLine\n";
    if (pdb->isLoaded())
    {
        for (unsigned int i = 0; i < pdb->Atoms.size(); ++i)
        {
            Atom atm = pdb->Atoms[i];
            VectorThree XYZ = atm.getXYZ();        
            float density = ccp4->getDensity(XYZ);    
            string line = atm.getLine();     
            int atmNo = atm.AtomNo;                                                                                   
            cout << "" << density << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << atmNo << "," << line << "\n";
        }
    }
    cout << "END_ATOMDENSITY\n";   

}

void CoutReports::coutSlices(Ccp4* ccp4, PdbFile* pdb,VectorThree central, VectorThree linear, VectorThree planar,double width,double gap)
{
    SpaceTransformation space(central,linear,planar);
    //dummy use of slice function
    //DEBUG CHECK
    VectorThree ccc = space.applyTransformation(central);
    VectorThree ccr = space.reverseTransformation(central);
    VectorThree lll = space.applyTransformation(linear);
    VectorThree llr = space.reverseTransformation(linear);
    VectorThree ppp = space.applyTransformation(planar);
    VectorThree ppr = space.reverseTransformation(planar);
    //////////////
    cout << "BEGIN_DENSITYSLICE\n";    
    int length = width / gap;
    int halfLength = length/2;
    cout << "i,j,Density\n";
    for (int i = -1*halfLength; i <= halfLength; ++i)
    {
        for (int j = -1*halfLength; j <= halfLength; ++j)
        {
            double x0 = (i*gap);
            double y0 = (j*gap);
            double z0 = 0;            
            VectorThree transformed = space.applyTransformation(VectorThree(x0,y0,z0));            
            double density = ccp4->getDensity(transformed);
            cout << i+halfLength << "," << j+halfLength << "," << density << "\n";            
        }        
    }
    cout << "END_DENSITYSLICE\n";

    cout << "BEGIN_RADIANTSLICE\n";    
    cout << "i,j,Radiant\n";
    for (int i = -1*halfLength; i <= halfLength; ++i)
    {
        for (int j = -1*halfLength; j <= halfLength; ++j)
        {
            double x0 = (i*gap);
            double y0 = (j*gap);
            double z0 = 0;            
            VectorThree transformed = space.applyTransformation(VectorThree(x0,y0,z0));            
            double radiant = ccp4->getRadiant(transformed);
            cout << i+halfLength << "," << j+halfLength << "," << radiant << "\n";
        }        
    }
    cout << "END_RADIANTSLICE\n";

    cout << "BEGIN_LAPLACIANSLICE\n";    
    cout << "i,j,Laplacian\n";
    for (int i = -1*halfLength; i <= halfLength; ++i)
    {
        for (int j = -1*halfLength; j <= halfLength; ++j)
        {
            double x0 = (i*gap);
            double y0 = (j*gap);
            double z0 = 0;            
            VectorThree transformed = space.applyTransformation(VectorThree(x0,y0,z0));            
            double laplacian = ccp4->getLaplacian(transformed);
            cout << i+halfLength << "," << j+halfLength << "," << laplacian << "\n";
        }        
    }
    cout << "END_LAPLACIANSLICE\n";
}