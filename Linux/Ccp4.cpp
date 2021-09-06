
/************************************************************************
* RSA 4.9.21
* Because we are using this from CGI scripts in python, the return value is everything from cout
************************************************************************/
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cmath>

#include "Ccp4.h"
#include "VectorThree.h"

using namespace std;


Ccp4::Ccp4(string pdbCode, string directory)
{
    PI = 3.14159265;
	_loaded = false;	
	_resolution = 0.0;

    _pdbCode = pdbCode;
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
    infile.read((char*)&_w05_NXSTART, sizeof(_w05_NXSTART));    
    infile.read((char*)&_w06_NYSTART, sizeof(_w06_NYSTART));    
    infile.read((char*)&_w07_NZSTART, sizeof(_w07_NZSTART));    
    infile.read((char*)&_w08_MX, sizeof(_w08_MX));    
    infile.read((char*)&_w09_MY, sizeof(_w09_MY));    
    infile.read((char*)&_w10_MZ, sizeof(_w10_MZ));
    float w11_CELLA_X = 0.0;
    infile.read((char*)&w11_CELLA_X, sizeof(w11_CELLA_X));
    float w12_CELLA_Y = 0.0;
    infile.read((char*)&w12_CELLA_Y, sizeof(w12_CELLA_Y));
    float w13_CELLA_Z = 0.0;
    infile.read((char*)&w13_CELLA_Z, sizeof(w13_CELLA_Z));
    _w14_CELLB_X = 0.0;
    infile.read((char*)&_w14_CELLB_X, sizeof(_w14_CELLB_X));
    _w15_CELLB_Y = 0.0;
    infile.read((char*)&_w15_CELLB_Y, sizeof(_w15_CELLB_Y));
    _w16_CELLB_Z = 0.0;
    infile.read((char*)&_w16_CELLB_Z, sizeof(_w16_CELLB_Z));    
    infile.read((char*)&_w17_MAPC, sizeof(_w17_MAPC));    
    infile.read((char*)&_w18_MAPR, sizeof(_w18_MAPR));    
    infile.read((char*)&_w19_MAPS, sizeof(_w19_MAPS));
    _w17_MAPC -= 1;
    _w18_MAPR -= 1;
    _w19_MAPS -= 1;
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
    //we don;t want any of the rest of this, but we want the last bit as long as the matrix is:
    vector<float> tmpData;
    float bulk = 0.0;
    while (infile.read((char*)&bulk, sizeof(float)))
    {        
        tmpData.push_back(bulk);
    }
    infile.close();
    _loaded = true;
    
    int len = _w01_NX * _w02_NY * _w03_NZ;        
    int startBulk = tmpData.size() - len;
    int count = 0;
    for (unsigned int i = startBulk; i < tmpData.size(); ++i)
    {
        float mtx = tmpData[i];
        _matrix.push_back(mtx);
        _matrixPeaks.push_back(pair<float, int>(mtx,count));        
        count++;
    }
    calculateOrthoMat(w11_CELLA_X, w12_CELLA_Y, w13_CELLA_Z, _w14_CELLB_X, _w15_CELLB_Y, _w16_CELLB_Z);
    calculateOrigin(_w05_NXSTART,_w06_NYSTART,_w07_NZSTART,_w17_MAPC,_w18_MAPR,_w19_MAPS);
               
    _map2xyz.push_back(0);
    _map2xyz.push_back(0);
    _map2xyz.push_back(0);
    _map2xyz[_w17_MAPC] = 0;
    _map2xyz[_w18_MAPR] = 1;
    _map2xyz[_w19_MAPS] = 2;
    
    _map2crs.push_back(0);
    _map2crs.push_back(0);
    _map2crs.push_back(0);
    _map2crs[0] = _w17_MAPC;
    _map2crs[1] = _w18_MAPR;
    _map2crs[2] = _w19_MAPS;
    
    _cellDims.push_back(0.0);
    _cellDims.push_back(0.0);
    _cellDims.push_back(0.0);
    _cellDims[0] = w11_CELLA_X;
    _cellDims[1] = w12_CELLA_Y;
    _cellDims[2] = w13_CELLA_Z;
    
    _axisSampling.push_back(0);
    _axisSampling.push_back(0);
    _axisSampling.push_back(0);
    _axisSampling[0] = _w08_MX;
    _axisSampling[1] = _w09_MY;
    _axisSampling[2] = _w10_MZ;

    _crsStart.push_back(0);
    _crsStart.push_back(0);
    _crsStart.push_back(0);
    _crsStart[0] = _w05_NXSTART;
    _crsStart[1] = _w06_NYSTART;
    _crsStart[2] = _w07_NZSTART;
    
    _dimOrder.push_back(0);
    _dimOrder.push_back(0);
    _dimOrder.push_back(0);
    _dimOrder[0] = _w01_NX;
    _dimOrder[1] = _w02_NY;
    _dimOrder[2] = _w03_NZ;    
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



void Ccp4::makePeaks(PdbFile* pdbFile)
{
    sort(_matrixPeaks.rbegin(), _matrixPeaks.rend());

    unsigned int maxdensity = 500;
    if (_matrixPeaks.size() < maxdensity)
        maxdensity = _matrixPeaks.size();

    cout << "Density,C,R,S,X,Y,Z,NearestAtom,Distance\n";


    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        int pos = _matrixPeaks[i].second;
        vector<int> coords = getCRS(pos);
        VectorThree XYZ = getXYZ(coords[0], coords[1], coords[2]);
        float density = _matrixPeaks[i].first;
        double distance = 0;
        string line = "-";
        if (pdbFile->isLoaded())
        {
            Atom* atm = pdbFile->getNearest(XYZ.A, XYZ.B, XYZ.C);
            if (atm != NULL)
            {
                line = atm->getLine();
                distance = atm->distance(XYZ.A, XYZ.B, XYZ.C);
            }                    
        }
        if (line == "-")
            cout << "" << density << "," << coords[0] << "," << coords[1] << "," << coords[2] << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << line << ",-" << "\n";
        else
            cout << "" << density << "," << coords[0] << "," << coords[1] << "," << coords[2] << "," << XYZ.A << "," << XYZ.B << "," << XYZ.C << "," << line << "," << distance << "\n";
    }




}

float Ccp4::getDensity(int C, int R, int S)
{
    stringstream ss;
    ss << C << "," << R << "," << S;
    return 0.0;// _matrixMap[ss.str()];
}



/*******************************************************
* ****** PRIVATE HELPER INTERFACE *********************
*******************************************************/
int Ccp4::getPosition(int C, int R, int S)
{
    return 0;
}

vector<int> Ccp4::getCRS(int position)
{
    int sliceSize = _w01_NX * _w02_NY;
    int i = position / sliceSize;
    int remainder = position % sliceSize;
    int j = remainder / _w01_NX;
    int k = remainder % _w01_NX;
    vector<int> CRS;
    CRS.push_back(i);
    CRS.push_back(j);
    CRS.push_back(k);
    return CRS;
}

void Ccp4::calculateOrthoMat(float w11_CELLA_X, float w12_CELLA_Y, float w13_CELLA_Z, float w14_CELLB_X, float w15_CELLB_Y, float w16_CELLB_Z)
{
    // Cell angles is w14_CELLB_X, w15_CELLB_Y, w16_CELLB_Z
    // Cell lengths is w11_CELLA_X , w12_CELLA_Y , w13_CELLA_Z 
    double alpha = PI / 180 * w14_CELLB_X;
    double beta = PI / 180 * w15_CELLB_Y;
    double gamma = PI / 180 * w16_CELLB_Z;
    double temp = sqrt(1 - pow(cos(alpha), 2) - pow(cos(beta), 2) - pow(cos(gamma), 2) + 2 * cos(alpha) * cos(beta) * cos(gamma));

    double v00 = w11_CELLA_X;
    double v01 = w12_CELLA_Y * cos(gamma);
    double v02 = w13_CELLA_Z * cos(beta);
    double v10 = 0;
    double v11 = w12_CELLA_Y * sin(gamma);
    double v12 = w13_CELLA_Z * (cos(alpha) - cos(beta) * cos(gamma)) / sin(gamma);
    double v20 = 0;
    double v21 = 0;
    double v22 = w13_CELLA_Z * temp / sin(gamma);

    _orthoMat.putValue(w11_CELLA_X, 0, 0);
    _orthoMat.putValue(w12_CELLA_Y * cos(gamma), 0, 1);
    _orthoMat.putValue(w13_CELLA_Z * cos(beta), 0, 2);
    _orthoMat.putValue(0, 1, 0);
    _orthoMat.putValue(w12_CELLA_Y * sin(gamma), 1, 1);
    _orthoMat.putValue(w13_CELLA_Z * (cos(alpha) - cos(beta) * cos(gamma)) / sin(gamma), 1, 2);
    _orthoMat.putValue(0, 2, 0);
    _orthoMat.putValue(0, 2, 1);
    _orthoMat.putValue( w13_CELLA_Z * temp / sin(gamma), 2, 2);
    _deOrthoMat = _orthoMat.getInverse();
}


VectorThree Ccp4::getCRS(double x, double y, double z)
{    
    VectorThree vXYZIn; 
    VectorThree vCRS;
    
    vXYZIn.A = x;
    vXYZIn.B = y;
    vXYZIn.C = z;
    
    //If the axes are all orthogonal            
    if (_w14_CELLB_X == 90 && _w15_CELLB_Y == 90 && _w16_CELLB_Z == 90)
    {
        for (int i = 0; i < 3; ++i)
        {            
            double startVal = vXYZIn.getByIndex(i) - _origin.getByIndex(i);
            startVal /= _cellDims[i] / _axisSampling[i];
            //vCRS[i] = startVal;
            vCRS.putByIndex(i, startVal);
        }
    }
    else // they are not orthogonal
    {        
        VectorThree vFraction = _deOrthoMat.multiply(vXYZIn);
        for (int i = 0; i < 3; ++i)
        {     
            double val = vFraction.getByIndex(i) * _axisSampling[i] - _crsStart[_map2xyz[i]];     
            vCRS.putByIndex(i,val);
        }
    }    
    double c = vCRS.getByIndex(_map2crs[0]);
    double r = vCRS.getByIndex(_map2crs[1]);
    double s = vCRS.getByIndex(_map2crs[2]);
    
    VectorThree CRS;
    CRS.A = c;
    CRS.B = r;
    CRS.C = s;    
    return CRS;

}
VectorThree Ccp4::getXYZ(double c, double r, double s)
{    
    VectorThree vXYZ;    
    VectorThree vCRSIn;
        
    vCRSIn.A = c;
    vCRSIn.B = r;
    vCRSIn.C = s;
    //If the axes are all orthogonal            
    if (_w14_CELLB_X == 90 && _w15_CELLB_Y == 90 && _w16_CELLB_Z == 90)
    {
        for (int i = 0; i < 3; ++i)
        {    
            double startVal = vCRSIn.getByIndex(_map2xyz[i]);
            startVal *= _cellDims[i] / _axisSampling[i];    
            startVal += _origin.getByIndex(i);
            vXYZ.putByIndex(i,startVal);    
        }
    }
    else // they are not orthogonal
    {    
        VectorThree vCRS;    
        for (int i = 0; i < 3; ++i)
        {
            double startVal = 0;
            if (_w17_MAPC == i)
                startVal = _w05_NXSTART + c;
            else if (_w18_MAPR == i)
                startVal = _w06_NYSTART + r;
            else
                startVal = _w07_NZSTART + s;    
            vCRS.putByIndex(i,startVal);
        }    
        vCRS.putByIndex(0,vCRS.getByIndex(0) / _w08_MX);
        vCRS.putByIndex(1, vCRS.getByIndex(1) / _w09_MY);
        vCRS.putByIndex(2, vCRS.getByIndex(2) / _w10_MZ);
        vXYZ = _orthoMat.multiply(vCRS);    
    }        
    return vXYZ;
}

void Ccp4::calculateOrigin(int w05_NXSTART, int w06_NYSTART, int w07_NZSTART, int w17_MAPC, int w18_MAPR, int w19_MAPS)
{
    /****************************
    * These comments are from my C# version and I have no idea currently what they mean (RSA 6/9/21)
    * ******************************
     *TODO I am ignoring the possibility of passing in the origin for nowand using the dot product calc for non orthoganality.
     *The origin is perhaps used for cryoEM only and requires orthoganility
     *CRSSTART is w05_NXSTART, w06_NYSTART, w07_NZSTART             
     *Cell dims w08_MX, w09_MY, w10_MZ;            
     *Map of indices from crs to xyz is w17_MAPC, w18_MAPR, w19_MAPS
     */
    
    VectorThree oro;
    
    for (int i = 0; i < 3; ++i)
    {
        int startVal = 0;
        if (w17_MAPC == i)
            startVal = w05_NXSTART;
        else if (w18_MAPR == i)
            startVal = w06_NYSTART;
        else
            startVal = w07_NZSTART;
        
        oro.putByIndex(i, startVal);
    }
    oro.putByIndex(0, oro.getByIndex(0) / _w08_MX);
    oro.putByIndex(1, oro.getByIndex(1) / _w09_MY);
    oro.putByIndex(2, oro.getByIndex(2) / _w10_MZ);                
    _origin = _orthoMat.multiply(oro);    
}




