
/************************************************************************
* RSA 4.9.21
************************************************************************/
#include<iostream>
#include<fstream>

#include "Ccp4.h"
using namespace std;


Ccp4::Ccp4(string pdbCode, string directory)
{
	_pdbCode = pdbCode;
	_loaded = true;
	_resolution = 0.78;
	_directory = directory;
	//Load the binary data
	ifstream infile;
	infile.open(_directory + pdbCode + ".ccp4", ios::binary | ios::in);
	int buffer[1024];
	while (infile.read((char*)&buffer, sizeof(buffer)))
	{
		cout << (char*)&buffer;
	}
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
