#pragma once
#include <string>

using namespace std;
class Cpp4
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

