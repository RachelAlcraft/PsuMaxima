
/************************************************************************
* RSA 6.9.21
* Because we are using this from CGI scripts in python, the return value is everything from cout
************************************************************************/
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>

#include "PdbFile.h"
using namespace std;

PdbFile::PdbFile(string pdbCode, string directory)
{
	_pdbCode = pdbCode;
    _loaded = false;
	string fileName = directory + "pdb" + pdbCode + ".ent";
	ifstream myfile(fileName.c_str());

	if (myfile.is_open())
	{
		string line = "";
		while (getline(myfile, line))
		{
			//Add HOH, ATOM and HETATOM for now
			int posHET = line.find("HETATM");
			int posATM = line.find("ATOM");
			int posHOH = line.find("HOH");

			if (posHET == 0 || posATM == 0 || posHOH == 0)
				Atoms.push_back(Atom(line,true));
            //else
            //    cout << line << "\n";
		}
		myfile.close();
        cout << "Atoms size=" << Atoms.size() << "\n";
		_loaded = true;
	}

}

bool PdbFile::isLoaded()
{
	return _loaded;
}

string PdbFile::getPdbCode()
{
	return _pdbCode;
}

Atom* PdbFile::getNearest(double x, double y, double z)
{
	if (Atoms.size() > 0)
	{
		Atom* nearest = &Atoms[0];
		double neardistance = nearest->distance(x, y, z);
		for (unsigned int i = 1; i < Atoms.size(); ++i)
		{
			Atom* atm = &Atoms[i];
			if (atm->Element != "H")
			{
				double distance = atm->distance(x, y, z);
				if (distance < neardistance)
				{
					nearest = atm;
					neardistance = distance;
				}
			}
		}
		if (neardistance < 1.1)
			return nearest;
		else
			return NULL;
	}
	else
		return NULL;
	
}
