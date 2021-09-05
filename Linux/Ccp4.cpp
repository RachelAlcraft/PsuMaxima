
/************************************************************************
* RSA 4.9.21
************************************************************************/
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>

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
    infile.open((_directory + pdbCode + ".ccp4").c_str(), ios::binary | ios::in);

    //This opens the WORDS in the ccp4	    
    infile.read((char*)&_w01_NX, sizeof(_w01_NX));
    infile.read((char*)&_w02_NY, sizeof(_w02_NY));
    infile.read((char*)&_w03_NZ, sizeof(_w03_NZ));
    int MODE = 0;
    infile.read((char*)&MODE, sizeof(MODE));
    int w05_NXSTART = 0;
    infile.read((char*)&w05_NXSTART, sizeof(w05_NXSTART));
    int w06_NYSTART = 0;
    infile.read((char*)&w06_NYSTART, sizeof(w06_NYSTART));
    int w07_NZSTART = 0;
    infile.read((char*)&w07_NZSTART, sizeof(w07_NZSTART));
    int w08_MX = 0;
    infile.read((char*)&w08_MX, sizeof(w08_MX));
    int w09_MY = 0;
    infile.read((char*)&w09_MY, sizeof(w09_MY));
    int w10_MZ = 0;
    infile.read((char*)&w10_MZ, sizeof(w10_MZ));
    float w11_CELLA_X = 0.0;
    infile.read((char*)&w11_CELLA_X, sizeof(w11_CELLA_X));
    float w12_CELLA_Y = 0.0;
    infile.read((char*)&w12_CELLA_Y, sizeof(w12_CELLA_Y));
    float w13_CELLA_Z = 0.0;
    infile.read((char*)&w13_CELLA_Z, sizeof(w13_CELLA_Z));
    float w14_CELLB_X = 0.0;
    infile.read((char*)&w14_CELLB_X, sizeof(w14_CELLB_X));
    float w15_CELLB_Y = 0.0;
    infile.read((char*)&w15_CELLB_Y, sizeof(w15_CELLB_Y));
    float w16_CELLB_Z = 0.0;
    infile.read((char*)&w16_CELLB_Z, sizeof(w16_CELLB_Z));
    int w17_MAPC = 0;
    infile.read((char*)&w17_MAPC, sizeof(w17_MAPC));
    int w18_MAPR = 0;
    infile.read((char*)&w18_MAPR, sizeof(w18_MAPR));
    int w19_MAPS = 0;
    infile.read((char*)&w19_MAPS, sizeof(w19_MAPS));
    float w20_DMIN = 0.0;
    infile.read((char*)&w20_DMIN, sizeof(w20_DMIN));
    float w21_DMAX = 0.0;
    infile.read((char*)&w21_DMAX, sizeof(w21_DMAX));
    float w22_DMEAN = 0.0;
    infile.read((char*)&w22_DMEAN, sizeof(w22_DMEAN));
    int ISPG = 0;
    infile.read((char*)&ISPG, sizeof(ISPG));
    int NYSYMBT = 0;
    infile.read((char*)&NYSYMBT, sizeof(NYSYMBT));
    int EXTTYP = 0;
    infile.read((char*)&EXTTYP, sizeof(EXTTYP));
    int NVERSION = 0;
    infile.read((char*)&NVERSION, sizeof(NVERSION));
    float ORIGIN_X = 0.0;
    infile.read((char*)&ORIGIN_X, sizeof(ORIGIN_X));
    float ORIGIN_Y = 0.0;
    infile.read((char*)&ORIGIN_X, sizeof(ORIGIN_Y));
    float ORIGIN_Z = 0.0;
    infile.read((char*)&ORIGIN_Z, sizeof(ORIGIN_Z));
    //we don;t want any of the rest of this
    float bulk = 0.0;
    for (int i = 0; i < 267; ++i)
        infile.read((char*)&bulk, sizeof(bulk));

    float mtx = 0.0;
    int count = 0;
    while (infile.read((char*)&mtx, sizeof(float)))
    {
        _matrix.push_back(mtx);
        _matrixPeaks.push_back(pair<float, int>(mtx,count));
        count++;
    }
    infile.close();    
    sort(_matrixPeaks.begin(), _matrixPeaks.end());
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

//Weird but becuase we are returning via cmake to p[ython, we just print out the results

void Ccp4::makePeaks()
{    
    unsigned int maxdensity = 50;
    if (_matrixPeaks.size() < maxdensity)
        maxdensity = _matrixPeaks.size();

    cout << std::setprecision(6);
    cout << _pdbCode << ",CRS,Density,NearestAtom,Distance\n";


    for (unsigned int i = 1; i <= maxdensity; ++i)
    {
        int coords = _matrixPeaks[_matrixPeaks.size()-i].second;
        float density = _matrixPeaks[_matrixPeaks.size()-i].first;
        cout << "-," << coords << "," << std::setprecision(6) << density << ",-,-\n";
    }




}

float Ccp4::getDensity(int C, int R, int S)
{
    stringstream ss;
    ss << C << "," << R << "," << S;
    return 0.0;// _matrixMap[ss.str()];
}









