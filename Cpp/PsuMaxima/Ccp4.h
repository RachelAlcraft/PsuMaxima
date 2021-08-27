#pragma once

#include <string>
#include <vector>
#include <map>
#include <fstream>

using namespace std;

class Ccp4
{
private:
	double _resolution = 0;	
	bool _loaded = false;
public:
	Ccp4(string ccp4, string diff);
	double Resolution();
	bool Loaded();
};
