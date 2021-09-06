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
	string _line;
	double _x;
	double _y;
	double _z;

	// HELPER FUNCTIONS
	string trim(string string_to_trim);

public:
	Atom(string line);
	double distance(double x, double y, double z);
	string getLine();

	//Lazy public access functions
	string Element;
};

