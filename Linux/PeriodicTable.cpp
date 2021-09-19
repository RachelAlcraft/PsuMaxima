#include "PeriodicTable.h"

vector<double> PeriodicTable::getCromerMannCoefficients(string atomType)
{
	string element = getElement(atomType);
    
    if (element == "H")
        return vector<double>{ 0.493002, 0.322912, 0.140191, 0.04081, 10.5109, 26.1257, 3.14236, 57.7997, 0.003038 };
    if (element == "C")
        return vector<double>{  2.31, 1.02, 1.5886, 0.865, 20.8439, 10.2075, 0.5687, 51.6512, 0.2156  };
    if (element == "N")
        return vector<double>{ 12.2126, 3.1322, 2.0125, 1.1663, 0.0057, 9.8933, 28.9975, 0.5826, -11.529 };
    if (element == "O")
        return vector<double>{ 3.0485, 2.2868, 1.5463, 0.867, 13.2771, 5.7011, 0.3239, 32.9089, 0.2508 };
    if (element == "S")
        return vector<double>{ 6.9053, 5.2034, 1.4379, 1.5863, 1.4679, 22.2151, 0.2536, 56.172, 0.8669 };        
	
    return vector<double>();
}

string PeriodicTable::getElement(string atomType)
{
    string elem;
    elem.push_back(atomType[0]);
    return elem;
}
