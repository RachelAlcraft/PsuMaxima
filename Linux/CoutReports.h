#pragma once
/************************************************************************
* RSA 10.9.21
************************************************************************/

#include <string>
#include <vector>

#include "Ccp4.h"
#include "PdbFile.h"
#include "Interpolator.h"

using namespace std;

class CoutReports
{
private:

public:		
    static void coutPeaks(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, int interpNum);
    static void coutAtomsDensity(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp);
    static void coutAtomsAdjusted(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp);
    static void coutSlices(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar,double width,double gap);
    static void coutSyntheticSlice(string atoms, string model, Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar, double width, double gap);
    static void coutSyntheticIAM(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp);
    static void coutText(Ccp4* ccp4);
};