#pragma once
/************************************************************************
* RSA 12.9.21
* SyntheticDensity is an abstract class with multiple implementations, including 
Independent Atom Model (IAM)
Bond Electron Model (BEM)
Multipole (not yet)
************************************************************************/

#include <string>
#include <vector>

#include "Atom.h"

using namespace std;

class SyntheticDensity
{
protected:
	vector<Atom> _atoms;	
public:
	SyntheticDensity(vector<Atom> atoms);
	virtual double getElectronDensity(double x, double y, double z) = 0;
	//There will also be structure factor functions
};

class IAM:public SyntheticDensity
{
protected:	
public:
	IAM(vector<Atom> atoms);
	virtual double getElectronDensity(double x, double y, double z);	
};