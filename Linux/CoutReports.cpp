

/************************************************************************
* RSA 10.9.21
************************************************************************/

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <iomanip>

#include "VectorThree.h"
#include "helper.h"
#include "SpaceTransformation.h"

#include "CoutReports.h"

using namespace std;


void CoutReports::coutPeaks(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, int interpNum)
{
    sort(ccp4->MatrixPeaks.rbegin(), ccp4->MatrixPeaks.rend());
    vector<pair<float, int> > tmpMatrixPeaks;

    //Simply look around each point to see if it is the biggest
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
    // now create a list of interpolated peaks
    vector<pair<pair<float, VectorThree>,pair<float, VectorThree> > > tmpInterpPeaks;//Both density and laplacian adjusted
    unsigned int maxdensity = 10000;
    if (ccp4->MatrixPeaks.size() < maxdensity)
        maxdensity = ccp4->MatrixPeaks.size();
    
    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        pair<float,VectorThree> densityPair;
        pair<float,VectorThree> laplacianPair;
        int pos = ccp4->MatrixPeaks[i].second;        
        VectorThree Pcoords = ccp4->getCRS(pos);
        float Pdensity = ccp4->MatrixPeaks[i].first;                
        
        if (interpNum > 1)
        {
            VectorThree Dcoords = ccp4->getNearestPeak(Pcoords, interp, true);            
            double Ddensity = interp->getValue(Dcoords.C, Dcoords.B, Dcoords.A);
            densityPair.second = Dcoords;
            densityPair.first = Ddensity;
            //And we should also do this on a laplacian basis but for now I am just using the same thing TODO
            VectorThree Lcoords = ccp4->getNearestPeak(Pcoords, interp, false);
            double laplacian = interp->getLaplacian(Lcoords.C, Lcoords.B, Lcoords.A);
            laplacianPair.second = Lcoords;
            laplacianPair.first = laplacian;
        }
        else
        {
            densityPair.second = Pcoords;
            densityPair.first = Pdensity;
            //And we should also do this on a laplacian basis but for now I am just using the same thing TODO
            double laplacian = interp->getLaplacian(Pcoords.C, Pcoords.B, Pcoords.A);
            laplacianPair.second = Pcoords;
            laplacianPair.first = laplacian;

        }

        tmpInterpPeaks.push_back(pair<pair<float, VectorThree>,pair<float, VectorThree> >(densityPair,laplacianPair));

    }
    //https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html
    //"REMARK   1                                                                      "
    //"HETATM  286  O   HOH B  57      17.652   2.846  -0.887  1.00 28.92           O  "
    cout << "BEGIN_CHIMERAPEAKS\n";
    cout << "REMARK   1 Peaks for " << pdb->getPdbCode() << " calculated by Leucippus (Birkbeck College 2021)\n";    
    cout << "REMARK   2 Some documentation\n";    
    cout << "REMARK   3 some more\n";    
    int atomNo = 0;
    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        ++atomNo;
        pair<float, VectorThree> densityPair = tmpInterpPeaks[i].first;
        pair<float, VectorThree> laplacianPair = tmpInterpPeaks[i].second;
                
        VectorThree coords = densityPair.second;
        float density = densityPair.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.C, coords.B, coords.A);
        //FIRST THE DENSITY PEAKS        
        cout << helper::getWordStringGaps("HETATM",6) << "HETATM";                                      //1. Atom or Hetatm                
        cout << helper::getNumberStringGaps(atomNo,0,5) << atomNo;                                  //2. Atom no - 7        
        cout << helper::getWordStringGaps("PK",3) << "PK";                                          //3. Atom type, eg CA, CB...        
        cout << helper::getWordStringGaps("DEN",6) << "DEN";                                        //4. Amino Acid        
        cout << helper::getWordStringGaps("P",2)<< "P";                                            //5. Chain        
        cout << helper::getNumberStringGaps(atomNo,0,4) << atomNo;                                  //6. Residue number        
        cout << helper::getNumberStringGaps(XYZ.A,3,12) << setprecision(3) << fixed << XYZ.A;       //7. x coord
        cout << helper::getNumberStringGaps(XYZ.B,3,8) << setprecision(3) << fixed << XYZ.B;        //8. y coord
        cout << helper::getNumberStringGaps(XYZ.C,3,8) << setprecision(3) << fixed << XYZ.C;        //9. z coord                        
        cout << helper::getNumberStringGaps(1,2,6) << "1.00";                                       //10. Occupancy        
        cout << helper::getNumberStringGaps(density,2,6) << setprecision(2) << fixed << density;    //11. BFactor,which is really density        
        cout << helper::getWordStringGaps("H",12) << "H";                                           //12. Element     
        cout << "  \n";
        //THEN the laplacian peaks which are currenly the same TODO
        ++atomNo;
        VectorThree coordsL = laplacianPair.second;
        float laplacian = laplacianPair.first;
        XYZ = ccp4->getXYZFromCRS(coordsL.C, coordsL.B, coordsL.A);
        cout << helper::getWordStringGaps("HETATM",6) << "HETATM";                                      //1. Atom or Hetatm                
        cout << helper::getNumberStringGaps(atomNo,0,5) << atomNo;                                  //2. Atom no - 7        
        cout << helper::getWordStringGaps("PK",3) << "PK";                                          //3. Atom type, eg CA, CB...        
        cout << helper::getWordStringGaps("LAP",6) << "LAP";                                        //4. Amino Acid        
        cout << helper::getWordStringGaps("P",2)<< "P";                                            //5. Chain        
        cout << helper::getNumberStringGaps(atomNo,0,4) << atomNo;                                  //6. Residue number        
        cout << helper::getNumberStringGaps(XYZ.A,3,12) << setprecision(3) << fixed << XYZ.A;       //7. x coord
        cout << helper::getNumberStringGaps(XYZ.B,3,8) << setprecision(3) << fixed << XYZ.B;        //8. y coord
        cout << helper::getNumberStringGaps(XYZ.C,3,8) << setprecision(3) << fixed << XYZ.C;        //9. z coord                        
        cout << helper::getNumberStringGaps(1,2,6) << "1.00";                                       //10. Occupancy        
        cout << helper::getNumberStringGaps(laplacian*-1,2,6) << setprecision(2) << fixed << laplacian*-1;    //11. BFactor,which is really density        
        cout << helper::getWordStringGaps("H",12) << "H";                                           //12. Element     
        cout << "  \n";
    }
       /*http://www.bmsc.washington.edu/CrystaLinks/man/pdb/part_72.html
                 1         2         3         4         5         6         7
        1234567890123456789012345678901234567890123456789012345678901234567890
        MASTER       40    0    0    0    0    0    0    6 2930    2    0   29
        */                      
    cout << helper::getWordStringGaps("MASTER",6) << "MASTER";//1 -  6       Record name    "MASTER"             
    cout << helper::getNumberStringGaps(3,0,9) << 3;//11 - 15       Integer        numRemark     Number of REMARK records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//16 - 20       Integer        "0"
    cout << helper::getNumberStringGaps(0,0,5) << 0;//21 - 25       Integer        numHet        Number of HET records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//26 - 30       Integer        numHelix      Number of HELIX records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//31 - 35       Integer        numSheet      Number of SHEET records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//36 - 40       Integer        numTurn       Number of TURN records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//41 - 45       Integer        numSite       Number of SITE records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//46 - 50       Integer        numXform      Number of coordinate transformation  records (ORIGX+SCALE+MTRIX)
    cout << helper::getNumberStringGaps(atomNo,0,5) << atomNo;//51 - 55       Integer        numCoord      Number of atomic coordinate records (ATOM+HETATM)
    cout << helper::getNumberStringGaps(0,0,5) << 0;//56 - 60       Integer        numTer        Number of TER records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//61 - 65       Integer        numConect     Number of CONECT records
    cout << helper::getNumberStringGaps(0,0,5) << 0;//66 - 70       Integer        numSeq        Number of SEQRES records
    cout << "\nEND\n";
    cout << "END_CHIMERAPEAKS\n";
        
    cout << "BEGIN_ALLPEAKS\n";
    cout << "Density,C,R,S,X,Y,Z,NearestAtom,Distance\n";
    for (unsigned int i = 0; i < maxdensity; ++i)
    {
                
        VectorThree coords = tmpInterpPeaks[i].first.second;
        float density = tmpInterpPeaks[i].first.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.C, coords.B, coords.A);
        
        
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
        VectorThree coords = tmpInterpPeaks[i].first.second;
        float density = tmpInterpPeaks[i].first.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.C, coords.B, coords.A);

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

void CoutReports::coutAtoms(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp)
{
    cout << "BEGIN_ATOMDENSITY\n";
    cout << "Density,X,Y,Z,AtomNo,AtomLine\n";
    if (pdb->isLoaded())
    {
        for (unsigned int i = 0; i < pdb->Atoms.size(); ++i)
        {
            Atom atm = pdb->Atoms[i];
            VectorThree XYZ = atm.getXYZ();        
            //float density = ccp4->getDensity(XYZ);    
            VectorThree crs = ccp4->getCRSFromXYZ(XYZ);
            double density = interp->getValue(crs.A, crs.B, crs.C);
            string line = atm.getLine();     
            int atmNo = atm.AtomNo;                                                                                   
            cout << "" << density << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << atmNo << "," << line << "\n";
        }
    }
    cout << "END_ATOMDENSITY\n";   

}

void CoutReports::coutSlices(Ccp4* ccp4, PdbFile* pdb,Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar,double width,double gap)
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
            //double density2 = ccp4->getDensity(transformed);
            VectorThree crs = ccp4->getCRSFromXYZ(transformed);
            double density = interp->getValue(crs.A, crs.B, crs.C);
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
            //double radiant2 = ccp4->getRadiant(transformed);
            VectorThree crs = ccp4->getCRSFromXYZ(transformed);
            double radiant = interp->getRadiant(crs.A, crs.B, crs.C);
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
            //double laplacian1 = ccp4->getLaplacian(transformed);
            VectorThree crs = ccp4->getCRSFromXYZ(transformed);
            double laplacian = interp->getLaplacian(crs.A, crs.B, crs.C);
            cout << i+halfLength << "," << j+halfLength << "," << laplacian << "\n";
        }        
    }
    cout << "END_LAPLACIANSLICE\n";
}