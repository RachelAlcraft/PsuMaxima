#pragma once

/************************************************************************
* RSA 4.9.21
************************************************************************/

#include <string>
#include <vector>
using namespace std;

class Ccp4
{
private:
	bool _loaded = false;
	string _pdbCode = "";
	double _resolution = 0.0;
	//SETINGS
	string _directory = "";

	//THE "WORDS" from the Ccp4 file
	int _w01_NX = 0;
	int _w02_NY = 0;
	int _w03_NZ = 0;

	//The matrix data
	vector<float> _matrix;

public:
	Ccp4(string pdbCode, string directory);
	double getResolution();
	bool isLoaded();
	string getPdbCode();
};

const int makeConst(const int& num);

