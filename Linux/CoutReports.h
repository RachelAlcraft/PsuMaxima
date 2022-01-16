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
    static void coutSlices(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, vector<VectorThree> centrals, vector<VectorThree> linears, vector<VectorThree> planars,double width,double gap);
    static void coutSyntheticSlices(string atoms, string model, Interpolator* interp, vector<VectorThree> centrals, vector<VectorThree> linears, vector<VectorThree> planars, double width, double gap);
    static void coutSyntheticIAM(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp);
    static void coutDeformation(Ccp4* ccp4, PdbFile* pdb, Interpolator* interpMap, Interpolator* interpSample);
    static void coutSamples(Ccp4* ccp4, PdbFile* pdb, Interpolator* interpMap, Interpolator* interpSample);
    static void coutText(Ccp4* ccp4,bool cap500);
    static void coutEmbellishPdb(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, int interpNum);

//internal
    static void coutSlice(Ccp4* ccp4, PdbFile* pdb, Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar, double width, double gap, int position);
    static void coutSyntheticSlice(Interpolator* interp, VectorThree central, VectorThree linear, VectorThree planar, double width, double gap, int position);

    
};