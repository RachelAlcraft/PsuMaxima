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
	double _startx;
	double _starty;
	double _startz;
	double _endx;
	double _endy;
	double _endz;	
	int _motionNum;
	double _arcHeight;
	vector<VectorThree> _motionPositions1;
	vector<VectorThree> _motionPositions2;
	
	// HELPER FUNCTIONS
	string trim(string string_to_trim);
	void makeSyntheticAtom(string line);
	void makePdbAtom(string line);
	//synthetic density functons	
	double getDensityComponent(double d, double x, double y);
	double getIAMDensityInternal(VectorThree ABC, VectorThree XYZ, double occupancy);

public:	
    Atom(string line, bool fromPdb);//couild be apdb line or a synthetic line
	double distance(double x, double y, double z);
	string getLine();
    VectorThree getXYZ();
	double getIAMDensity(VectorThree XYZ);
	string info();

    //Lazy public access functions    
    int AtomNo;	
	string AtomType;
	int ResNo;
	string Element;
	double BFactor;
	double Occupancy;
	//there culd be end positions for motion
	bool MotionLine;
    
};

