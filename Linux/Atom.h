#pragma once

/************************************************************************
* RSA 6.9.21
************************************************************************/

#include <string>
#include <vector>

using namespace std;

class Atom
{
private:
	string _line = "";
	double _x = 0.0;
	double _y = 0.0;
	double _z = 0.0;

public:
	Atom(string line);
	double distance(double x, double y, double z);
	string getLine();
};

