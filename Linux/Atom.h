#pragma once

/************************************************************************
* RSA 6.9.21
************************************************************************/

#include <string>
#include <vector>
#include "VectorThree.h"

using namespace std;

class Atom
{
private:
	string _line;
	double _x;
	double _y;
	double _z;
	
	// HELPER FUNCTIONS
	string trim(string string_to_trim);
	void makeSyntheticAtom(string line);
	void makePdbAtom(string line);
	//synthetic density functons	
	double getDensityComponent(double d, double x, double y);

public:	
    Atom(string line, bool fromPdb);//couild be apdb line or a synthetic line
	double distance(double x, double y, double z);
	string getLine();
    VectorThree getXYZ();
	double getIAMDensity(VectorThree XYZ);

    //Lazy public access functions    
    int AtomNo;	
	string AtomType;
	int ResNo;
	string Element;
	double BFactor;
	double Occupancy;
    
};

