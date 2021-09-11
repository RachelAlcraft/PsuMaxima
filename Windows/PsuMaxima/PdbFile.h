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
	bool _loaded;
	string _pdbCode;

	//SETINGS
	string _directory;

public:
	//Useful to loop outside, bad code
	vector<Atom> Atoms;

	PdbFile(string pdbCode, string directory);
	bool isLoaded();
	string getPdbCode();
	Atom* getNearest(double x, double y, double z);
};

