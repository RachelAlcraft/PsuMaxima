

/************************************************************************
* RSA 10.9.21
************************************************************************/

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <iomanip>
#include <cmath>

#include "VectorThree.h"
#include "helper.h"
#include "SpaceTransformation.h"

#include "CoutReports.h"

using namespace std;


void CoutReports::coutPeaks(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, int interpNum)
{
    ccp4->CreatePeaks(interp,interpNum);

    unsigned int maxdensity = 9999;
    if (ccp4->DenLapPeaks.size() < maxdensity)
        maxdensity = (int)ccp4->DenLapPeaks.size();
                
    //https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html
    //"REMARK   1                                                                      "
    //"HETATM  286  O   HOH B  57      17.652   2.846  -0.887  1.00 28.92           O  "
    cout << "BEGIN_CHIMERAPEAKS\n";
    cout << "REMARK   1 Peaks for " << pdb->getPdbCode() << " calculated by Leucippus (Birkbeck University of London 2021).\n";    
    cout << "REMARK   2 Software developed by Rachel Alcraft (2021) - supervisor Mark A. Williams.\n";    
    cout << "REMARK   3 Dummy atoms positioned at peaks calculated using both density and the laplacian.\n";    
    cout << "REMARK   4 All atoms have dummy type PK; element H; and chain P.\n";    
    cout << "REMARK   5 Residue DEN is for density calculated peaks and LAP for laplacian calculated.\n"; 
    int atomNo = 0;
    int resNo = 0;
    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        ++atomNo;
        ++resNo;
        pair<double, VectorThree> densityPair = ccp4->DenLapPeaks[i].first;
        pair<double, VectorThree> laplacianPair = ccp4->DenLapPeaks[i].second;
                
        VectorThree coords = densityPair.second;
        double density = densityPair.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.reverse());
        //FIRST THE DENSITY PEAKS        
        cout << helper::getWordStringGaps("HETATM",6) << "HETATM";                                      //1. Atom or Hetatm                
        cout << helper::getNumberStringGaps(atomNo,0,5) << atomNo;                                  //2. Atom no - 7        
        cout << helper::getWordStringGaps("PK",3) << "PK";                                          //3. Atom type, eg CA, CB...        
        cout << helper::getWordStringGaps("DEN",6) << "DEN";                                        //4. Amino Acid        
        cout << helper::getWordStringGaps("P",2)<< "P";                                            //5. Chain        
        cout << helper::getNumberStringGaps(resNo,0,4) << resNo;                                  //6. Residue number        
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
        double laplacian = laplacianPair.first;
        XYZ = ccp4->getXYZFromCRS(coordsL.reverse());
        cout << helper::getWordStringGaps("HETATM",6) << "HETATM";                                      //1. Atom or Hetatm                
        cout << helper::getNumberStringGaps(atomNo,0,5) << atomNo;                                  //2. Atom no - 7        
        cout << helper::getWordStringGaps("PK",3) << "PK";                                          //3. Atom type, eg CA, CB...        
        cout << helper::getWordStringGaps("LAP",6) << "LAP";                                        //4. Amino Acid        
        cout << helper::getWordStringGaps("P",2)<< "P";                                            //5. Chain        
        cout << helper::getNumberStringGaps(resNo,0,4) << resNo;                                  //6. Residue number        
        cout << helper::getNumberStringGaps(XYZ.A,3,12) << setprecision(3) << fixed << XYZ.A;       //7. x coord
        cout << helper::getNumberStringGaps(XYZ.B,3,8) << setprecision(3) << fixed << XYZ.B;        //8. y coord
        cout << helper::getNumberStringGaps(XYZ.C,3,8) << setprecision(3) << fixed << XYZ.C;        //9. z coord                        
        cout << helper::getNumberStringGaps(1,2,6) << "1.00";                                       //10. Occupancy        
        cout << helper::getNumberStringGaps(laplacian*-1.00,2,6) << setprecision(2) << fixed << laplacian*-1;    //11. BFactor,which is really density        
        cout << helper::getWordStringGaps("H",12) << "H";                                           //12. Element     
        cout << "  \n";
    }
       /*http://www.bmsc.washington.edu/CrystaLinks/man/pdb/part_72.html
                 1         2         3         4         5         6         7
        1234567890123456789012345678901234567890123456789012345678901234567890
        MASTER       40    0    0    0    0    0    0    6 2930    2    0   29
        */                      
    cout << helper::getWordStringGaps("MASTER",6) << "MASTER";//1 -  6       Record name    "MASTER"             
    cout << helper::getNumberStringGaps(4,0,9) << 5;//11 - 15       Integer        numRemark     Number of REMARK records
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
                
        VectorThree coords = ccp4->DenLapPeaks[i].first.second;
        double density = ccp4->DenLapPeaks[i].first.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.reverse());
        
        
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
        VectorThree coords = ccp4->DenLapPeaks[i].first.second;
        double density = ccp4->DenLapPeaks[i].first.first;
        VectorThree XYZ = ccp4->getXYZFromCRS(coords.reverse());

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

void CoutReports::coutAtomsDensity(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp)
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
void CoutReports::coutAtomsAdjusted(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp)
{    
    if (pdb->isLoaded())
    {
        cout << "BEGIN_DENSITYADJUSTED\n";
        cout << "REMARK   1 Atom positions for " << pdb->getPdbCode() << " adjusted on density maxima by Leucippus (Birkbeck University of London 2021).\n";
        cout << "REMARK   2 Software developed by Rachel Alcraft (2021) - supervisor Mark A. Williams.\n";
        cout << "REMARK   3 Only atoms with full occupancy have been included.\n";
        cout << "REMARK   4 Where a nearby density peak could not be found the atom has been removed\n";

        int numAtoms = 0;
        for (unsigned int i = 0; i < pdb->Atoms.size(); ++i)
        {
            Atom atm = pdb->Atoms[i];
            if (atm.peakable("DEN"))
            {
                VectorThree CRS = ccp4->getCRSFromXYZ(atm.getXYZ());                
                VectorThree ABC = interp->getNearbyAtomPeak(CRS.reverse(), true);                
                if (ABC.Valid) 
                {
                    VectorThree XYZ = ccp4->getXYZFromCRS(ABC.reverse());
                    ++numAtoms;
                    string line = atm.getLineCoords(XYZ);
                    cout << line << "\n";
                }
            }            
        }
        cout << helper::getWordStringGaps("MASTER", 6) << "MASTER";//1 -  6       Record name    "MASTER"             
        cout << helper::getNumberStringGaps(4, 0, 9) << 4;//11 - 15       Integer        numRemark     Number of REMARK records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//16 - 20       Integer        "0"
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//21 - 25       Integer        numHet        Number of HET records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//26 - 30       Integer        numHelix      Number of HELIX records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//31 - 35       Integer        numSheet      Number of SHEET records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//36 - 40       Integer        numTurn       Number of TURN records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//41 - 45       Integer        numSite       Number of SITE records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//46 - 50       Integer        numXform      Number of coordinate transformation  records (ORIGX+SCALE+MTRIX)
        cout << helper::getNumberStringGaps(numAtoms, 0, 5) << numAtoms;//51 - 55       Integer        numCoord      Number of atomic coordinate records (ATOM+HETATM)
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//56 - 60       Integer        numTer        Number of TER records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//61 - 65       Integer        numConect     Number of CONECT records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//66 - 70       Integer        numSeq        Number of SEQRES records
        cout << "END_DENSITYADJUSTED\n";

        cout << "BEGIN_LAPLACIANADJUSTED\n";
        cout << "REMARK   1 Atom positions for " << pdb->getPdbCode() << " adjusted on laplacian minima by Leucippus (Birkbeck University of London 2021).\n";
        cout << "REMARK   2 Software developed by Rachel Alcraft (2021) - supervisor Mark A. Williams.\n";
        cout << "REMARK   3 Only atoms with full occupancy have been included.\n";
        cout << "REMARK   4 Where a nearby laplacian peak could not be found the atom has been removed\n";

        numAtoms = 0;
        for (unsigned int i = 0; i < pdb->Atoms.size(); ++i)
        {
            Atom atm = pdb->Atoms[i];
            if (atm.peakable("LAP"))
            {
                VectorThree CRS = ccp4->getCRSFromXYZ(atm.getXYZ());
                VectorThree ABC = interp->getNearbyAtomPeak(CRS.reverse(), false);                
                if (ABC.Valid)
                {
                    VectorThree XYZ = ccp4->getXYZFromCRS(ABC.reverse());
                    ++numAtoms;
                    string line = atm.getLineCoords(XYZ);
                    cout << line << "\n";
                }
            }
        }
        cout << helper::getWordStringGaps("MASTER", 6) << "MASTER";//1 -  6       Record name    "MASTER"             
        cout << helper::getNumberStringGaps(4, 0, 9) << 4;//11 - 15       Integer        numRemark     Number of REMARK records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//16 - 20       Integer        "0"
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//21 - 25       Integer        numHet        Number of HET records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//26 - 30       Integer        numHelix      Number of HELIX records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//31 - 35       Integer        numSheet      Number of SHEET records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//36 - 40       Integer        numTurn       Number of TURN records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//41 - 45       Integer        numSite       Number of SITE records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//46 - 50       Integer        numXform      Number of coordinate transformation  records (ORIGX+SCALE+MTRIX)
        cout << helper::getNumberStringGaps(numAtoms, 0, 5) << numAtoms;//51 - 55       Integer        numCoord      Number of atomic coordinate records (ATOM+HETATM)
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//56 - 60       Integer        numTer        Number of TER records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//61 - 65       Integer        numConect     Number of CONECT records
        cout << helper::getNumberStringGaps(0, 0, 5) << 0;//66 - 70       Integer        numSeq        Number of SEQRES records
        cout << "END_LAPLACIANADJUSTED\n";
    }
    


}

void CoutReports::coutSlices(Ccp4* ccp4, PdbFile* pdb,Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar,double width,double gap)
{
    SpaceTransformation space(central,linear,planar);
    //dummy use of slice function
        
    //////////////
    cout << "BEGIN_DENSITYSLICE\n";    
    int length = (int)(width / gap);
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

    //FINALLY CRATE THE position matrix
    cout << "BEGIN_POSITIONSLICE\n";
    cout << "i,j,Position\n";
    //we do not need a massive matrix of zeros, these positions go with the above, so we fill with zeros and then place these points
    VectorThree ccc = space.reverseTransformation(central);    
    VectorThree lll = space.reverseTransformation(linear);    
    VectorThree ppp = space.reverseTransformation(planar);
    ccc = ccc/gap;
    ccc.A += (double)halfLength;
    ccc.B += halfLength;    
    int x = (int)ccc.A;
    int y = (int)ccc.B;
    double val = 1;
    if (abs(ccc.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    lll = lll/gap;
    lll.A += (double)halfLength;
    lll.B += halfLength;    
    x = (int)lll.A;
    y = (int)lll.B;
    val = 1;
    if (abs(lll.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    ppp = ppp/gap;
    ppp.A += (double)halfLength;
    ppp.B += halfLength;    
    x = (int)ppp.A;
    y = (int)ppp.B;
    val = 1;
    if (abs(ppp.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    
    cout << "END_POSITIONSLICE\n";

}

void CoutReports::coutSyntheticIAM(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp)
{
    interp->addAtoms(pdb->Atoms);
    cout << "BEGIN_SYNTHETIC_IAM\n";
    cout << "i,j,k,Density\n";
    cout << ccp4->W01_NX << "," << ccp4->W02_NY << "," << ccp4->W03_NZ << ",Dimensions\n";
    for (int i = 0; i < ccp4->W01_NX; ++i)
    {
        for (int j = 0; j < ccp4->W02_NY; ++j)
        {
            for (int k = 0; k < ccp4->W03_NZ; ++k)
            {
                VectorThree XYZ = ccp4->getXYZFromCRS(VectorThree(i,j,k).reverse());
                double val = interp->getValue(XYZ.A, XYZ.B, XYZ.C);
                double absval = abs(val);
                if (absval > 0.0001)
                    cout << i << "," << j << "," << k << "," << val <<"\n";
            }
        }
    }

    cout << "END_SYNTHETIC_IAM\n";

}

void CoutReports::coutSyntheticSlice(string atoms, string model, Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar, double width, double gap)
{
    //The atoms are a list of lines
    if (atoms.size() > 2)
    {
        vector<string> lines = helper::stringToVector(atoms, "@");
        //we want to turn each line ibnto a synthetic atom

        vector<Atom> atomsList;
        for (unsigned int i = 0; i < lines.size(); ++i)
        {
            string line = lines[i];
            if (line.size() > 5)
            {
                atomsList.push_back(Atom(line, false));
            }
        }

        interp->addAtoms(atomsList);

        cout << "BEGIN_ATOMDATA\n";
        cout << "AtomStrings\n";
        for (unsigned int i = 0; i < atomsList.size(); ++i)
            cout << atomsList[i].info() << "\n";
        cout << "END_ATOMDATA\n";
    }
    if (model == "BEM")
        interp->createBondElectrons();//will add bond electron pairs here when do that model TODO
    
  
    //CRETAE SYNTHETIC DENSITY SLICES
    SpaceTransformation space(central, linear, planar);            
    //////////////
    cout << "BEGIN_DENSITYSLICE\n";
    int length = (int)(width / gap);
    int halfLength = length / 2;
    cout << "i,j,Density\n";
    for (int i = -1 * halfLength; i <= halfLength; ++i)
    {
        for (int j = -1 * halfLength; j <= halfLength; ++j)
        {
            double x0 = (i * gap);
            double y0 = (j * gap);
            double z0 = 0;
            VectorThree transformed = space.applyTransformation(VectorThree(x0, y0, z0));            
            double density = interp->getValue(transformed.A, transformed.B, transformed.C);
            cout << i + halfLength << "," << j + halfLength << "," << density << "\n";
        }
    }
    cout << "END_DENSITYSLICE\n";

    cout << "BEGIN_RADIANTSLICE\n";
    cout << "i,j,Radiant\n";
    for (int i = -1 * halfLength; i <= halfLength; ++i)
    {
        for (int j = -1 * halfLength; j <= halfLength; ++j)
        {
            double x0 = (i * gap);
            double y0 = (j * gap);
            double z0 = 0;
            VectorThree transformed = space.applyTransformation(VectorThree(x0, y0, z0));            
            double radiant = interp->getRadiant(transformed.A, transformed.B, transformed.C);
            cout << i + halfLength << "," << j + halfLength << "," << radiant << "\n";
        }
    }
    cout << "END_RADIANTSLICE\n";

    cout << "BEGIN_LAPLACIANSLICE\n";
    cout << "i,j,Laplacian\n";
    for (int i = -1 * halfLength; i <= halfLength; ++i)
    {
        for (int j = -1 * halfLength; j <= halfLength; ++j)
        {
            double x0 = (i * gap);
            double y0 = (j * gap);
            double z0 = 0;
            VectorThree transformed = space.applyTransformation(VectorThree(x0, y0, z0));            
            double laplacian = interp->getLaplacian(transformed.A, transformed.B, transformed.C);
            cout << i + halfLength << "," << j + halfLength << "," << laplacian << "\n";
        }
    }
    cout << "END_LAPLACIANSLICE\n";

    //FINALLY CRATE THE position matrix
    cout << "BEGIN_POSITIONSLICE\n";
    cout << "i,j,Position\n";
    //we do not need a massive matrix of zeros, these positions go with the above, so we fill with zeros and then place these points
    VectorThree ccc = space.reverseTransformation(central);    
    VectorThree lll = space.reverseTransformation(linear);    
    VectorThree ppp = space.reverseTransformation(planar);
    ccc = ccc/gap;
    ccc.A += (double)halfLength;
    ccc.B += halfLength;    
    int x = (int)ccc.A;
    int y = (int)ccc.B;
    double val = 1;
    if (abs(ccc.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    lll = lll/gap;
    lll.A += (double)halfLength;
    lll.B += halfLength;    
    x = (int)lll.A;
    y = (int)lll.B;
    val = 1;
    if (abs(lll.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    ppp = ppp/gap;
    ppp.A += (double)halfLength;
    ppp.B += halfLength;    
    x = (int)ppp.A;
    y = (int)ppp.B;
    val = 1;
    if (abs(ppp.C > 0.01))
        val = 0.5;//non-planar
    cout << x << "," << y << "," << val << "\n";

    
    cout << "END_POSITIONSLICE\n";

}

void CoutReports::coutText(Ccp4* ccp4)
{
    ccp4->coutText();
}
