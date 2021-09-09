#include <cmath>
#include <stdlib.h> 

#include "Atom.h"

using namespace std;

Atom::Atom(string line)
{
	_line = line;

	// 7 - 11        Integer       serial       Atom  serial number.
	AtomNo = atol(trim(line.substr(6, 5)).c_str());
	//13 - 16        Atom          name         Atom name.
	string elementName = trim(line.substr(12, 4));
	//16 - 17        The accupancy code if there is one
	string occupant = trim(line.substr(16, 1));
	//18 - 20        Residue name  resName      Residue name.
	string aminoCode = trim(line.substr(17, 3)); // or nucleic code this is not accurate
	//22             Character     chainID      Chain identifier.
	string chainId = trim(line.substr(21, 1));
	//23 - 26        Integer       resSeq       Residue sequence number.
	int resNo = atol(trim(line.substr(22, 5)).c_str());
	//27        Insertion of mmutations
	string insertion = trim(line.substr(26, 1)).c_str();
	//31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
	//39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
	//47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
	string x_c = trim(line.substr(30, 8));
	string y_c = trim(line.substr(38, 8));
	string z_c = trim(line.substr(46, 8));
	_x = atof(x_c.c_str());
	_y = atof(y_c.c_str());
	_z = atof(z_c.c_str());	
	//55 - 60        Real(8.3)     occupancy   Double
	string occ = trim(line.substr(54, 6));
	double occupancy = atof(occ.c_str());	
	//61 - 66        Real(8.3)     b factor   Double
	string bfac = trim(line.substr(60, 6));
	double bfactor = atof(bfac.c_str());
	//77 - 78        LString(2)    element      Element symbol, right-justified.
	Element = "";
	if (line.length() > 76)
		Element = trim(line.substr(76, 2));

}

double Atom::distance(double x, double y, double z)
{
	return sqrt(pow(x - _x, 2) + pow(y - _y, 2) + pow(z - _z, 2));
}

string Atom::getLine()
{
	return _line;
}

VectorThree Atom::getXYZ()
{
    VectorThree xyz;
    xyz.A = _x;
    xyz.B = _y;
    xyz.C = _z;
    return xyz;
}

string Atom::trim(string string_to_trim)
{
	string string_trimmed = string_to_trim;
	size_t startpos = string_trimmed.find_first_not_of(" ");
	size_t endpos = string_trimmed.find_last_not_of(" ");
	if (startpos == string::npos)
		string_trimmed = "";
	else if (endpos == string::npos)
		string_trimmed = string_trimmed.substr(startpos);
	else
		string_trimmed = string_trimmed.substr(startpos, endpos - startpos + 1);
	return string_trimmed;
}