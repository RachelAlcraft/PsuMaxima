#include <math.h>

#include "Atom.h"

using namespace std;

Atom::Atom(string line)
{
	_line = line;
}

double Atom::distance(double x, double y, double z)
{
	return sqrt(pow(x - _x,2) + pow(y - _y,2) + pow(z - _z,2));
}

string Atom::getLine()
{
	return _line;
}
