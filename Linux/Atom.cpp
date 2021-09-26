#define _USE_MATH_DEFINES
#include <cmath>
#include <stdlib.h> 
#include <sstream>
#include <iomanip>

#include "helper.h"
#include "PeriodicTable.h"
#include "Atom.h"

using namespace std;

Atom::Atom(string line, bool fromPdb)
{
	MotionLine = false;
	_line = line;
	if (fromPdb)	
		makePdbAtom(line);			
	else	
		makeSyntheticAtom(line);	
}

void Atom::makeSyntheticAtom(string line)
{
	//Type, X, Y, Z, ResNo, BFactor, Occupancy, EndX, EndY, EndZ, ArcHeight
	vector<string> inps = helper::stringToVector(line, ",");
	if (inps.size() >= 7)
	{
		AtomType = inps[0];
		_x = atof(inps[1].c_str());
		_y = atof(inps[2].c_str());
		_z = atof(inps[3].c_str());
		ResNo = atol(inps[4].c_str());
		BFactor = atof(inps[5].c_str());
		Occupancy = atof(inps[6].c_str());
	}
	MotionLine = false;
	if (inps.size() > 13)
	{
		_startx = atof(inps[7].c_str());
		_starty = atof(inps[8].c_str());
		_startz = atof(inps[9].c_str());
		_endx = atof(inps[10].c_str());
		_endy = atof(inps[11].c_str());
		_endz = atof(inps[12].c_str());
		_motionNum = atol(inps[13].c_str());		
		if (_motionNum > 0)
		{//under this model it spends slightly loner in the centre - by double
			MotionLine = true;				
			_motionPositions1 = getXYZ().getArcPositions(VectorThree(_startx,_starty,_startz),_motionNum);
			_motionPositions2 = getXYZ().getArcPositions(VectorThree(_endx,_endy,_endz),_motionNum);
		}
	}
}
void Atom::makePdbAtom(string line)
{
	// 7 - 11        Integer       serial       Atom  serial number.
	AtomNo = atol(trim(line.substr(6, 5)).c_str());
	//13 - 16        Atom          name         Atom name.
	AtomType = trim(line.substr(12, 4));
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
	Occupancy = atof(occ.c_str());
	//61 - 66        Real(8.3)     b factor   Double
	string bfac = trim(line.substr(60, 6));
	BFactor = atof(bfac.c_str());
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

double Atom::getIAMDensity(VectorThree XYZ)
{
	if (!MotionLine)
	{
		return getIAMDensityInternal(getXYZ(),XYZ,Occupancy);
	}
	else
	{
		double density = 0;
		double halfOcc = Occupancy/2.0;
		for (unsigned int i = 0; i < _motionPositions1.size(); ++i)
		{
			density+=getIAMDensityInternal(_motionPositions1[i],XYZ,halfOcc/_motionNum);
		}
		for (unsigned int i = 0; i < _motionPositions2.size(); ++i)
		{
			density+=getIAMDensityInternal(_motionPositions2[i],XYZ,halfOcc/_motionNum);
		}
		return density;
	}
	

}

double Atom::getIAMDensityInternal(VectorThree ABC, VectorThree XYZ, double occupancy)
{
	double DISTANCE_CAP = 5;
    /*
        https://www.phenix-online.org/presentations/latest/pavel_maps_2.pdf
        https://github.com/project-gemmi/gemmi/blob/master/include/gemmi/dencalc.hpp
        https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Modules_and_Websites_(Inorganic_Chemistry)/Crystallography/X-rays/CromerMann_coefficients

        rho(r) = sum(i = 1�4)
        a(i) * [4 * pi / (bi + B)] ^ 1.5
        * exp[-4 * pi ^ 2 * r ^ 2 / (bi + B)]

        + c * [4 * pi / B] ^ 1.5
        * exp[-4 * pi ^ 2 * r ^ 2 / B]

    */
	double distance = XYZ.distance(ABC);
    
    //let's decide that at a certain distance there is no need to do all thi calculation
    if (distance < DISTANCE_CAP || DISTANCE_CAP == 0)
    {
        double density = 0;
        vector<double> cromerMann = PeriodicTable::getCromerMannCoefficients(AtomType);
		if (cromerMann.size() > 1)
		{

			density += getDensityComponent(distance, cromerMann[0], (cromerMann[4] + BFactor));
			density += getDensityComponent(distance, cromerMann[1], (cromerMann[5] + BFactor));
			density += getDensityComponent(distance, cromerMann[2], (cromerMann[6] + BFactor));
			density += getDensityComponent(distance, cromerMann[3], (cromerMann[7] + BFactor));
			double c = cromerMann[8];
			c = getDensityComponent(distance, c, BFactor);
			if (!isnan((double)c))
				density += c;

			return occupancy * density;
		}
		else
			return 0;
    }
    else
    {
        return 0;
    }
}

double Atom::getDensityComponent(double d, double x, double y)
{
    /*
    rho(r) = sum(i = 1�4)
    a(i) * [4 * pi / (bi + B)] ^ 1.5
    * exp[-4 * pi ^ 2 * r ^ 2 / (bi + B)]

    + c * [4 * pi / B] ^ 1.5
    * exp[-4 * pi ^ 2 * r ^ 2 / B]

    Passed in:
    x * [4 * pi / y]^1.5 + exp[-4 * pi^2*r^2 / y]
    */
    if (abs(y) < 0.00001)
        return 0;

    double bottom = 4 * M_PI / y;
    double raised = pow(bottom, 3);
    raised = sqrt(raised);

    double index = 4 * pow(M_PI, 2) * pow(d, 2) / y;
    double exponent = exp(index);
	if (abs(exponent) < 0.00001)
		return 0;
    
	exponent = 1 / exponent;
    return x * raised * exponent;
}

string Atom::info()
{
	stringstream ss;
	double halfOcc = Occupancy/2.0;
	ss << AtomType << ":ResNo=" << ResNo << ":BF=" << BFactor << ":Occ=" << Occupancy;
	if (MotionLine)
	{
		ss << ":MotionLine=";
		for (unsigned int i = 0; i < _motionPositions1.size(); ++i)
		{
			ss << "\n:s:" << _motionPositions1[i].A << ":Occ=" << halfOcc/_motionNum;
		}
		for (unsigned int i = 0; i < _motionPositions2.size(); ++i)
		{
			ss << "\n:e:" << _motionPositions2[i].A << ":Occ=" << halfOcc/_motionNum;
		}

	}
	return ss.str();

}

bool Atom::peakable(string peakType)
{
	if (Occupancy < 1)
		return false;
	return true;
}
string Atom::getLineCoords(VectorThree coords)
{
	//ATOM   1735 HH21 ARG A 104      43.578 -16.554  97.660  1.00 23.80           H
	//HETATM28234  O   HOH F 699      14.045  -0.373 -23.581  1.00 34.10           O  
	//ATOM    664  N   ASN A  46      13.954   6.416  13.695  1.00  3.26           N  
	//HETATM  685  O  BEOH A  66      14.811   2.078  12.602  0.40  5.53           O  
	//HETATM    4 PK   LAP P   2      -7.998  18.130  -8.794  1.00107.49           H  
	string bgn = _line.substr(0, 26);	
	string end = _line.substr(54);
	stringstream ss;
	ss << helper::getNumberStringGaps(coords.A, 3, 12) << setprecision(3) << fixed << coords.A;
	ss << helper::getNumberStringGaps(coords.B, 3, 8) << setprecision(3) << fixed << coords.B;
	ss << helper::getNumberStringGaps(coords.C, 3, 8) << setprecision(3) << fixed << coords.C;
	return bgn + ss.str() + end;
}