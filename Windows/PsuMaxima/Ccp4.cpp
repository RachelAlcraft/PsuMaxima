
/************************************************************************
* RSA 4.9.21
************************************************************************/

#include "Ccp4.h"
using namespace std;


Ccp4::Ccp4(string pdbCode)
{
	_pdbCode = pdbCode;
	_loaded = true;
	_resolution = 0.78;
}
double Ccp4::getResolution()
{
	return _resolution;
}

bool Ccp4::isLoaded()
{
	return _loaded;
}

string Ccp4::getPdbCode()
{
	return _pdbCode;
}
