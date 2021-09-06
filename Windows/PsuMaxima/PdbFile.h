#pragma once

/************************************************************************
* RSA 6.9.21
************************************************************************/

#include <string>
#include <vector>
#include "Atom.h"

using namespace std;

class PdbFile
{
private:
	bool _loaded = false;
	string _pdbCode = "";	
	vector<Atom> _atoms;
	//SETINGS
	string _directory = "";

public:
	PdbFile(string pdbCode, string directory);	
	bool isLoaded();
	string getPdbCode();	
	Atom* getNearest(double x, double y, double z);
};

