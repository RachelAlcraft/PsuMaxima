
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
#include <cstring> // memcpy

#include "Ccp4.h"
#include "helper.h"
#include "VectorThree.h"
#include <iomanip>


using namespace std;

typedef unsigned char uchar;


Ccp4::Ccp4(string pdbCode, string type, string directory, int Fos, int Fcs)
{
    _type = type;
    _fos = Fos;
    _fcs = Fcs;
    _noMains = _fos + _fcs;
	_noDiffs = (_fos - _fcs) - (_fos + _noMains);
    
    if (_noDiffs != 0)
        loadDiffFile(pdbCode, directory);
            
    loadMainFile(pdbCode,directory);
    //now create the peaks matrix

    vector<float> tmpMatrix;
    for (unsigned int i = 0; i < Matrix.size(); ++i)
    {
        float mtx = Matrix[i];
        mtx *= _noMains;
        if (_noDiffs != 0)
        {
           mtx +=  _noDiffs * MatrixDiff[i];
        }
        tmpMatrix.push_back(mtx);
        //lets not bother to add it to the peaks if it is smaller than the mean
        if (mtx > _w22_DMEAN)
            MatrixPeaks.push_back(pair<float, int>(mtx, i));
        
    }
    Matrix = tmpMatrix;

}

/*void Ccp4::loadMainFile(string pdbCode, string directory)
{
    PI = 3.14159265;
    _loaded = false;
    _resolution = 0.0;
    _endian = isBigEndian();

    _pdbCode = pdbCode;
    _resolution = 0.78;
    _directory = directory;
    //Load the binary data

    //std::ifstream input((_directory + pdbCode + ".ccp4").c_str(), std::ios::binary);
    //std::vector<unsigned char> buffer(std::istreambuf_iterator<char>(input), {});

    ifstream infile;
    infile.open((_directory + pdbCode + ".ccp4").c_str(), ios::binary | ios::in);
    //This opens the WORDS in th  ccp4	    
    infile.read((char*)&W01_NX, sizeof(W01_NX));
    infile.read((char*)&W02_NY, sizeof(W02_NY));
    infile.read((char*)&W03_NZ, sizeof(W03_NZ));
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
    infile.read((char*)&_w22_DMEAN, sizeof(_w22_DMEAN));

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

    unsigned char temp[sizeof(float)];
    while (infile.read(reinterpret_cast<char*>(temp), sizeof(float)))
        //while (infile.read((char*)&bulk, sizeof(float)))
    {
        if (false) // big endian method???
        {
            unsigned char t = temp[0];
            temp[0] = temp[3];
            temp[3] = t;
            t = temp[1];
            temp[1] = temp[2];
            temp[2] = t;
            float bulk = reinterpret_cast<float&>(temp);
            tmpData.push_back(bulk);
        }
        else
        {
            float bulk = reinterpret_cast<float&>(temp);
            tmpData.push_back(bulk);
        }
    }
    infile.close();
    _loaded = true;

    int len = W01_NX * W02_NY * W03_NZ;
    int startBulk = (int)tmpData.size() - len;
    int count = 0;
    for (unsigned int i = startBulk; i < tmpData.size(); ++i)
    {
        float mtx = tmpData[i];
        Matrix.push_back(mtx);
        //lets not bother to add it to the peaks if it is smaller than the mean
        //if (mtx > _w22_DMEAN)
        //    MatrixPeaks.push_back(pair<float, int>(mtx, count));


        count++;
    }
    calculateOrthoMat(w11_CELLA_X, w12_CELLA_Y, w13_CELLA_Z, _w14_CELLB_X, _w15_CELLB_Y, _w16_CELLB_Z);
    calculateOrigin(_w05_NXSTART, _w06_NYSTART, _w07_NZSTART, _w17_MAPC, _w18_MAPR, _w19_MAPS);

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
    _dimOrder[0] = W01_NX;
    _dimOrder[1] = W02_NY;
    _dimOrder[2] = W03_NZ;
}*/
void Ccp4::loadMainFile(string pdbCode, string directory)
{
    PI = 3.14159265;
    _loaded = false;
    _resolution = 0.0;
    _endian = isBigEndian();

    _pdbCode = pdbCode;
    _resolution = 0.78;
    _directory = directory;

    createWordsData(_directory, _wordsDataStrMain, _wordsDataIntMain, _wordsDataFloatMain, false);
       
    W01_NX = _wordsDataIntMain[0];
    W02_NY = _wordsDataIntMain[1];
    W03_NZ = _wordsDataIntMain[2];
    _w05_NXSTART = _wordsDataIntMain[4];
    _w06_NYSTART = _wordsDataIntMain[5];
    _w07_NZSTART = _wordsDataIntMain[6];
    _w08_MX = _wordsDataIntMain[7];
    _w09_MY = _wordsDataIntMain[8];
    _w10_MZ = _wordsDataIntMain[9];
    float w11_CELLA_X = _wordsDataFloatMain[10];
    float w12_CELLA_Y = _wordsDataFloatMain[11];
    float w13_CELLA_Z = _wordsDataFloatMain[12];
    _w14_CELLB_X = _wordsDataFloatMain[13];
    _w15_CELLB_Y = _wordsDataFloatMain[14];
    _w16_CELLB_Z = _wordsDataFloatMain[15];
    _w17_MAPC = _wordsDataIntMain[16];
    _w18_MAPR = _wordsDataIntMain[17];
    _w19_MAPS = _wordsDataIntMain[18];
    _w17_MAPC -= 1;
    _w18_MAPR -= 1;
    _w19_MAPS -= 1;
    float w20_DMIN = _wordsDataFloatMain[19];
    float w21_DMAX = _wordsDataFloatMain[20];
    _w22_DMEAN = _wordsDataFloatMain[21];
    
    
    _loaded = true;
    int len = W01_NX * W02_NY * W03_NZ;
    int startBulk = (int)_wordsDataFloatMain.size() - len;
    int count = 0;
    for (unsigned int i = startBulk; i < _wordsDataFloatMain.size(); ++i)
    {
        float mtx = _wordsDataFloatMain[i];
        Matrix.push_back(mtx);        
        count++;
    }
    calculateOrthoMat(w11_CELLA_X, w12_CELLA_Y, w13_CELLA_Z, _w14_CELLB_X, _w15_CELLB_Y, _w16_CELLB_Z);
    calculateOrigin(_w05_NXSTART, _w06_NYSTART, _w07_NZSTART, _w17_MAPC, _w18_MAPR, _w19_MAPS);

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
    _dimOrder[0] = W01_NX;
    _dimOrder[1] = W02_NY;
    _dimOrder[2] = W03_NZ;
}
void Ccp4::loadDiffFile(string pdbCode, string directory)
{
    PI = 3.14159265;
    _loaded = false;
    _resolution = 0.0;
    _endian = isBigEndian();

    _pdbCode = pdbCode;
    _resolution = 0.78;
    _directory = directory;
    //Load the binary data
    createWordsData(_directory, _wordsDataStrDiff, _wordsDataIntDiff, _wordsDataFloatDiff,true);
    
    _loaded = false;
    _resolution = 0.0;
    _endian = isBigEndian();

    _pdbCode = pdbCode;
    _resolution = 0.78;
    _directory = directory;

    W01_NX = _wordsDataIntDiff[0];
    W02_NY = _wordsDataIntDiff[1];
    W03_NZ = _wordsDataIntDiff[2];

    _loaded = true;
    int len = W01_NX * W02_NY * W03_NZ;
    int startBulk = (int)_wordsDataFloatDiff.size() - len;
    int count = 0;
    for (unsigned int i = startBulk; i < _wordsDataFloatDiff.size(); ++i)
    {
        float mtx = _wordsDataFloatDiff[i];
        MatrixDiff.push_back(mtx);
        count++;
    }    
}
void Ccp4::createWordsList(int symmetry, int length, int nCnRnS)
{//https://ftp.ebi.ac.uk/pub/databases/emdb/doc/Map-format/current/EMDB_map_format.pdf
    //int unless otherwise stated
    _wordsList.push_back("1_NC");
    _wordsList.push_back("2_NR");
    _wordsList.push_back("3_NS");

    _wordsList.push_back("4_MODE");
    
    _wordsList.push_back("5_NCSTART");
    _wordsList.push_back("6_NRSTART");
    _wordsList.push_back("7_NSSTART");

    _wordsList.push_back("8_NX");
    _wordsList.push_back("9_NY");
    _wordsList.push_back("10_NZ");

    _wordsList.push_back("11_X_LENGTH");//float
    _wordsList.push_back("12_Y_LENGTH");//float
    _wordsList.push_back("13_Z_LENGTH");//float

    _wordsList.push_back("14_ALPHA");//float
    _wordsList.push_back("15_BETA");//float
    _wordsList.push_back("16_GAMMA");//float

    _wordsList.push_back("17_MAPC");
    _wordsList.push_back("18_MAPR");
    _wordsList.push_back("19_MAPS");

    _wordsList.push_back("20_AMIN");//float
    _wordsList.push_back("21_AMAX");//float
    _wordsList.push_back("22_AMEAN");//float

    _wordsList.push_back("23_ISPG");

    _wordsList.push_back("24_NYYMBT");//num of bytes in symmetry table
        
    _wordsList.push_back("25_LSKFLG");//skew flag

    _wordsList.push_back("26_SKWMAT_S11");//float, skew matrix
    _wordsList.push_back("27_SKWMAT_S12");//float, skew matrix
    _wordsList.push_back("28_SKWMAT_S13");//float, skew matrix
    _wordsList.push_back("29_SKWMAT_S21");//float, skew matrix
    _wordsList.push_back("30_SKWMAT_S22");//float, skew matrix
    _wordsList.push_back("31_SKWMAT_S23");//float, skew matrix
    _wordsList.push_back("32_SKWMAT_S31");//float, skew matrix
    _wordsList.push_back("33_SKWMAT_S32");//float, skew matrix
    _wordsList.push_back("34_SKWMAT_S33");//float, skew matrix

    _wordsList.push_back("35_SKWTRN_T1");//float, skew turn
    _wordsList.push_back("36_SKWTRN_T2");//float, skew turn
    _wordsList.push_back("37_SKWTRN_T3");//float, skew turn
    
    for (unsigned int i = 38; i < 53; ++i)
    {
        stringstream word;
        word << i << "_EXTRA";//binary
        _wordsList.push_back(word.str());
    }

    _wordsList.push_back("53_MAP");//char MRC or CCP4 I think
    _wordsList.push_back("54_MACHST");//binary machine stamp
    _wordsList.push_back("55_RMS");//float root mean square deviation
    _wordsList.push_back("56_NLABL");// num of labels

    for (unsigned int i = 57; i < 257; ++i)
    {
        stringstream word;
        word << i << "_LABEL";//binary
        _wordsList.push_back(word.str());
    }

    //symmetry info not EDMS XRAY only
    int startVoxels = length - nCnRnS+1;
    int symCount = 0;
    for (int i = 257; i < startVoxels; ++i)
    {
        ++symCount;
        stringstream word;
        word << symCount << "_SYM";//binary
        _wordsList.push_back(word.str());
    }
    //voxels we have to work out backwards from the data
    int voxCount = 0;
    for (int i = startVoxels; i < length+1; ++i)
    {
        ++voxCount;
        stringstream word;
        word << voxCount << "_VOXEL";//float
        _wordsList.push_back(word.str());
    }
    







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

float Ccp4::getDensity(int C, int R, int S)
{
    int pos = getPosition(C, R, S);
    return Matrix[pos];
}



void Ccp4::CreatePeaks(Interpolator* interp, int interpNum)
{
    /*
    * Some debug code to understand why a tryptohan 219 in 1us0 is missing peaks

    int pos1 = getPosition(87, 183, 119);
    int pos2 = getPosition(87, 182, 119);
    int pos3 = getPosition(87, 184, 119);
    int pos4 = getPosition(86, 183, 119);
    int pos5 = getPosition(88, 183, 119);
    int pos6 = getPosition(87, 183, 118);
    int pos7 = getPosition(87, 183, 120);

    float d1 = getDensity(87, 183, 119);
    float d2 = getDensity(87, 182, 119);
    float d3 = getDensity(87, 184, 119);
    float d4 = getDensity(86, 183, 119);
    float d5 = getDensity(88, 183, 119);
    float d6 = getDensity(87, 183, 118);
    float d7 = getDensity(87, 183, 120);*/
    /////////////////////////////////////////    
    vector<pair<float, int> > tmpMatrixPeaks;
    for (unsigned int i = 0; i < MatrixPeaks.size(); ++i)
    {
        double peak = MatrixPeaks[i].first;
        int position = MatrixPeaks[i].second;

        /*if (position == 8281847)
        {
            int breakpoint = 0;
            ++breakpoint;
        }*/

        VectorThree CRS = getCRS(position);
        bool are_any_bigger = false;
        for (int a = -1; a < 2; ++a)
        {
            for (int b = -1; b < 2; ++b)
            {
                for (int c = -1; c < 2; ++c)
                {
                    int tmpPos = getPosition(a + (int)CRS.A, b + (int)CRS.B, c + (int)CRS.C);
                    if (tmpPos > 0 && tmpPos < Matrix.size())
                    {
                        double tmpPeak = Matrix[tmpPos];
                        if (tmpPeak > peak)
                            are_any_bigger = true;
                    }

                }
            }
        }
        if (!are_any_bigger)
        {
            tmpMatrixPeaks.push_back(pair<float, int>(peak, position));
        }
    }
    MatrixPeaks = tmpMatrixPeaks;//Matrixpeaks are now sorted and actual peaks
    sort(MatrixPeaks.rbegin(), MatrixPeaks.rend());

    //Now we want to get density and laplacian for every peak
    vector<string> keyList;
    unsigned int maxdensity = 100000;
    if (MatrixPeaks.size() < maxdensity)
        maxdensity = (int)MatrixPeaks.size();

    for (unsigned int i = 0; i < maxdensity; ++i)
    {
        pair<double, VectorThree> densityPair;
        pair<double, VectorThree> laplacianPair;
        float Pdensity = MatrixPeaks[i].first;
        int pos = MatrixPeaks[i].second;
        VectorThree Pcoords = getCRS(pos);
        if (interpNum > 1)
        {
            VectorThree Dcoords = interp->getNearbyGridPeak(Pcoords,true);
            VectorThree Lcoords = interp->getNearbyGridPeak(Pcoords,false);
            if (Dcoords.Valid && Lcoords.Valid)
            {
                double density = interp->getValue(Dcoords.C, Dcoords.B, Dcoords.A);
                densityPair.second = Dcoords;
                densityPair.first = density;
                double laplacian = interp->getLaplacian(Lcoords.C, Lcoords.B, Lcoords.A);
                laplacianPair.second = Lcoords;
                laplacianPair.first = laplacian;
                DenLapPeaks.push_back(pair<pair<double, VectorThree>, pair<double, VectorThree> >(densityPair, laplacianPair));
            }
        }
        else
        {
            densityPair.second = Pcoords;
            densityPair.first = Pdensity;
            double laplacian = interp->getLaplacian(Pcoords.C, Pcoords.B, Pcoords.A);
            laplacianPair.second = Pcoords;
            laplacianPair.first = laplacian;
            DenLapPeaks.push_back(pair<pair<double, VectorThree>, pair<double, VectorThree> >(densityPair, laplacianPair));
        }
    }


}

void Ccp4::createWordsData(string directory, vector<string>& dataStr, vector<int>& dataInt, vector<float>& dataFloat, bool isDiff)
{
    ifstream infile;
    string filename = _directory + _pdbCode + ".ccp4";
    if (isDiff)
        filename = _directory + _pdbCode + "_diff.ccp4";

    infile.open(filename.c_str(), ios::binary | ios::in);    
    unsigned char temp[sizeof(float)];
    while (infile.read(reinterpret_cast<char*>(temp), sizeof(float)))
    {
        string ss(reinterpret_cast<char const*>(temp));
        float sf = reinterpret_cast<float&>(temp);
        int si = reinterpret_cast<int&>(temp);

        if (ss.size() > 8)        
            ss = ss.substr(8);
        
        
        int pos = ss.find(",");
        if (pos>0)
        {
            vector<string> sv = helper::stringToVector(ss,",");
            ss = "";
            for (unsigned int c=0;c<sv.size();++c)
            {
                ss += sv[c] + ".";
            }
        }

        dataStr.push_back(ss);
        dataFloat.push_back(sf);
        dataInt.push_back(si);
    }
    infile.close();
    int symmetry = dataInt[23]; //the length of the symmetry data is held here
    int length = (int)dataInt.size();
    int nCnRnS = dataInt[0] * dataInt[1] * dataInt[2];
    createWordsList(symmetry,length,nCnRnS);
}

void Ccp4::coutText(bool cap500)
{
    vector<string> textFile;
    int symmetry = _wordsDataIntMain[23]; //the length of the symmetry data is held here
    int length = (int)_wordsDataIntMain.size();
    int nCnRnS = _wordsDataIntMain[0] * _wordsDataIntMain[1] * _wordsDataIntMain[2];

    if (_wordsList.size() == _wordsDataIntMain.size())
    {
        cout << "BEGIN_RAWTEXT\n";
        cout << "Word,Data\n";

        //and print it out                
        cout << setprecision(8);
        int length = _wordsList.size();
        int end = _wordsList.size();
        if (length > 500 && cap500)
            end = 500;
        for (unsigned int i = 0; i < end; ++i)
        {
            cout << _wordsList[i] << ",";
            if (10 <= i && i < 16)
                cout << _wordsDataFloatMain[i] << "\n";
            else if (19 <= i && i < 22)
                cout << _wordsDataFloatMain[i] << "\n";
            else if (25 <= i && i < 37)
                cout << _wordsDataFloatMain[i] << "\n";
            else if (37 <= i && i < 54)
                cout << _wordsDataStrMain[i] << "\n";
            else if (i == 54)
                cout << _wordsDataFloatMain[i] << "\n";
            else if (i == 55)
                cout << _wordsDataIntMain[i] << "\n";
            else if (56 <= i && i < 256)
                cout << _wordsDataStrMain[i] << "\n";
            //symmetry
            else if (256 <= i && i < length - nCnRnS)
                cout << _wordsDataStrMain[i] << "\n";
            //voxels
            else if (i >= length - nCnRnS)//voxels
                cout << _wordsDataFloatMain[i] << "\n";
            else
                cout << _wordsDataIntMain[i] << "\n";


        }
        cout << "END_RAWTEXT\n";
    }
    else
    {
        cout << "Error in words creation";
    }

}

void Ccp4::printText(string directory,bool cap500)
{
    //createWordsData(directory);
    int symmetry = _wordsDataIntMain[23]; //the length of the symmetry data is held here
    int length = (int)_wordsDataIntMain.size();
    int nCnRnS = _wordsDataIntMain[0] * _wordsDataIntMain[1] * _wordsDataIntMain[2];

    if (_wordsList.size() == _wordsDataIntMain.size())
    {

        //and print it out
        ofstream outfile;
        string outfilename = _directory + _pdbCode + "_ccp4.txt";
        outfile.open(outfilename.c_str(), ios::out);
        outfile << setprecision(8);
        
        int end = _wordsList.size();
        if (length > 500 && cap500)
            end = 500;

        for (unsigned int i = 0; i < end; ++i)
        {
            outfile << _wordsList[i] << "=";
            if (10 <= i && i < 16)
                outfile << _wordsDataFloatMain[i] << "\n";
            else if (19 <= i && i < 22)
                outfile << _wordsDataFloatMain[i] << "\n";
            else if (25 <= i && i < 37)
                outfile << _wordsDataFloatMain[i] << "\n";
            else if (37 <= i && i < 54)
                outfile << _wordsDataStrMain[i] << "\n";
            else if (i == 54)
                outfile << _wordsDataFloatMain[i] << "\n";
            else if (i == 55)
                outfile << _wordsDataIntMain[i] << "\n";
            else if (56 <= i && i < 256)
                outfile << _wordsDataStrMain[i] << "\n";
            //symmetry
            else if (256 <= i && i < length - nCnRnS)
                outfile << _wordsDataStrMain[i] << "\n";
            //voxels
            else if (i >= length - nCnRnS)//voxels
                outfile << _wordsDataFloatMain[i] << "\n";
            else
                outfile << _wordsDataIntMain[i] << "\n";

            
        }
        outfile.close();
    }
    else
    {
        cout << "Error in words creation";
    }

}







/*******************************************************
* ****** PRIVATE HELPER INTERFACE *********************
*******************************************************/
int Ccp4::getPosition(int C, int R, int S)
{
    int sliceSize = W01_NX * W02_NY;
    int pos = C * sliceSize;
    pos += W01_NX * R;
    pos += S;
    return pos;
}

VectorThree Ccp4::getCRS(int position)
{
    int sliceSize = W01_NX * W02_NY;
    int i = position / sliceSize;
    int remainder = position % sliceSize;
    int j = remainder / W01_NX;
    int k = remainder % W01_NX;
    VectorThree CRS;
    CRS.A = i;
    CRS.B = j;
    CRS.C = k;
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
    _orthoMat.putValue(w13_CELLA_Z * temp / sin(gamma), 2, 2);
    _deOrthoMat = _orthoMat.getInverse();
    //VectorThree XYZ = getXYZFromCRS(10,10,10); DEBUG CODE
}


VectorThree Ccp4::getCRSFromXYZ(VectorThree XYZ)
{
    VectorThree vCRS;
    //If the axes are all orthogonal            
    if (_w14_CELLB_X == 90 && _w15_CELLB_Y == 90 && _w16_CELLB_Z == 90)
    {
        for (int i = 0; i < 3; ++i)
        {
            double startVal = XYZ.getByIndex(i) - _origin.getByIndex(i);
            startVal /= _cellDims[i] / _axisSampling[i];
            //vCRS[i] = startVal;
            vCRS.putByIndex(i, startVal);
        }
    }
    else // they are not orthogonal
    {
        VectorThree vFraction = _deOrthoMat.multiply(XYZ, true);
        for (int i = 0; i < 3; ++i)
        {
            double val = vFraction.getByIndex(i) * _axisSampling[i] - _crsStart[_map2xyz[i]];
            vCRS.putByIndex(i, val);
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
VectorThree Ccp4::getXYZFromCRS(VectorThree vCRSIn)
{
    VectorThree vXYZ;
        
    //If the axes are all orthogonal            
    if (_w14_CELLB_X == 90 && _w15_CELLB_Y == 90 && _w16_CELLB_Z == 90)
    {
        for (int i = 0; i < 3; ++i)
        {
            double startVal = vCRSIn.getByIndex(_map2xyz[i]);
            startVal *= _cellDims[i] / _axisSampling[i];
            startVal += _origin.getByIndex(i);
            vXYZ.putByIndex(i, startVal);
        }
    }
    else // they are not orthogonal
    {
        VectorThree vCRS;
        for (int i = 0; i < 3; ++i)
        {
            double startVal = 0;
            if (_w17_MAPC == i)
                startVal = _w05_NXSTART + vCRSIn.A;
            else if (_w18_MAPR == i)
                startVal = _w06_NYSTART + vCRSIn.B;
            else
                startVal = _w07_NZSTART + vCRSIn.C;
            vCRS.putByIndex(i, startVal);
        }
        vCRS.putByIndex(0, vCRS.getByIndex(0) / _w08_MX);
        vCRS.putByIndex(1, vCRS.getByIndex(1) / _w09_MY);
        vCRS.putByIndex(2, vCRS.getByIndex(2) / _w10_MZ);
        vXYZ = _orthoMat.multiply(vCRS, false);
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
    _origin = _orthoMat.multiply(oro, true);
}

bool Ccp4::isBigEndian()
{
    union
    {
        int  i;
        char b[sizeof(int)];
    } u;
    u.i = 1;
    return (u.b[0] == 1) ? true : false;
} 