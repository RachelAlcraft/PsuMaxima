#pragma once

/************************************************************************
* RSA 4.9.21
************************************************************************/

#include <string>
using namespace std;

class Ccp4
{
private:
	bool _loaded = false;
	string _pdbCode = "";
	double _resolution = 0.0;

public:
	Ccp4(string pdbCode);
	double getResolution();
	bool isLoaded();
	string getPdbCode();
};

