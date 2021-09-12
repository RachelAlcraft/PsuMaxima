#include "SyntheticDensity.h"

//****** ABSTRACT CLASS FOR SYNTHETIC DENSITY *******************//
SyntheticDensity::SyntheticDensity(vector<Atom> atoms)
{
	_atoms = atoms;
}

//****************************************************************************************
// Imprementation 1) Independent Atom Model
//****************************************************************************************
IAM::IAM(vector<Atom> atoms):SyntheticDensity(atoms)
{
}

double IAM::getElectronDensity(double x, double y, double z)
{
	return 0.0;
}
