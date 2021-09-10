#pragma once
/************************************************************************
* RSA 10.9.21
************************************************************************/

#include <string>
#include <vector>

#include "Ccp4.h"
#include "PdbFile.h"

using namespace std;

class CoutReports
{
private:

public:		
    static void coutPeaks(Ccp4* ccp4, PdbFile* pdb);
    static void coutAtoms(Ccp4* ccp4, PdbFile* pdb);
    static void coutSlices(Ccp4* ccp4, PdbFile* pdb,VectorThree central, VectorThree linear, VectorThree planar,double width,double gap);
};