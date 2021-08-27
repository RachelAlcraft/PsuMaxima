#include "Ccp4.h"

using namespace std;

Ccp4::Ccp4(string ccp4, string diff)
{
	_resolution = 0.8;
	//Attempt to load a binary file
	char buffer[100];
	ifstream myFile(ccp4, ios::in);// | ios::binary);
	myFile.read(buffer, 100);
	if (!myFile)
		_loaded = false;
	else
		_loaded = true;
}

double Ccp4::Resolution()
{
	return _resolution;
}

bool Ccp4::Loaded()
{
	return _loaded;
}