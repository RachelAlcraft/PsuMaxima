#include "PeriodicTable.h"

vector<double> PeriodicTable::getCromerMannCoefficients(string atomType)
{
    vector<double> cromers;
	string element = getElement(atomType);        
    if (element == "H")
        cromers.push_back(0.493002);
        cromers.push_back(0.322912);
        cromers.push_back(0.140191);
        cromers.push_back(0.04081);
        cromers.push_back(10.5109);
        cromers.push_back(26.1257);
        cromers.push_back(3.14236);
        cromers.push_back(57.7997);
        cromers.push_back(0.003038);    
    if (element == "C")
        cromers.push_back(2.31);
        cromers.push_back(1.02);
        cromers.push_back(1.5886);
        cromers.push_back(0.865);
        cromers.push_back(20.8439);
        cromers.push_back(10.2075);
        cromers.push_back(0.5687);
        cromers.push_back(51.6512);
        cromers.push_back(0.2156);
    if (element == "N")
        cromers.push_back(12.2126);
        cromers.push_back(3.1322);
        cromers.push_back(2.0125);
        cromers.push_back(1.1663);
        cromers.push_back(0.0057);
        cromers.push_back(9.8933);
        cromers.push_back(28.9975);
        cromers.push_back(0.5826);
        cromers.push_back(-11.529);
    if (element == "O")
        cromers.push_back(3.0485);
        cromers.push_back(2.2868);
        cromers.push_back(1.5463);
        cromers.push_back(0.867);
        cromers.push_back(13.2771);
        cromers.push_back(5.7011);
        cromers.push_back(0.3239);
        cromers.push_back(32.9089);
        cromers.push_back(0.2508);
    if (element == "S")
        cromers.push_back(6.9053);
        cromers.push_back(5.2034);
        cromers.push_back(1.4379);
        cromers.push_back(1.5863);
        cromers.push_back(1.4679);
        cromers.push_back(22.2151);
        cromers.push_back(0.2536);
        cromers.push_back(56.172);
        cromers.push_back(0.8669);
	
    return cromers;
}

string PeriodicTable::getElement(string atomType)
{
    string elem;
    elem.push_back(atomType[0]);
    return elem;
}
