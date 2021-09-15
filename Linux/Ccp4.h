#pragma once

/************************************************************************
* RSA 4.9.21
************************************************************************/

#include <string>
#include <vector>
#include <map>
#include "PdbFile.h"
#include "MatrixThreeThree.h"
#include "VectorThree.h"
#include "Interpolator.h"

using namespace std;

class Ccp4
{
private:
	bool _endian;
	double PI;
	bool _loaded;
	string _pdbCode;
	double _resolution;
	//SETINGS
	string _directory;

	//THE "WORDS" from the Ccp4 file	
public:
	int W01_NX;
	int W02_NY;
	int W03_NZ;
private:
	int _w05_NXSTART;
	int _w06_NYSTART;
	int _w07_NZSTART;
	int _w08_MX;
	int _w09_MY;
	int _w10_MZ;
	float _w14_CELLB_X;
	float _w15_CELLB_Y;
	float _w16_CELLB_Z;
	int _w17_MAPC;
	int _w18_MAPR;
	int _w19_MAPS;


	//Calculation data
	MatrixThreeThree _orthoMat;
	MatrixThreeThree _deOrthoMat;
	vector<int> _map2xyz;
	vector<int> _map2crs;
	vector<float>_cellDims;
	vector<int> _axisSampling;
	vector<int> _crsStart;
	vector<int> _dimOrder;
	VectorThree _origin;

	
	//Helper functioms	
	void calculateOrthoMat(float w11_CELLA_X, float w12_CELLA_Y, float w13_CELLA_Z, float w14_CELLB_X, float w15_CELLB_Y, float w16_CELLB_Z);
	void calculateOrigin(int w05_NXSTART, int w06_NYSTART, int w07_NZSTART, int w17_MAPC, int w18_MAPR, int w19_MAPS);
	bool isBigEndian();


public:
    //The matrix data lazily as a public accessor
	vector<float> Matrix;
	vector<pair<float, int> > MatrixPeaks;

public:
	Ccp4(string pdbCode, string directory);
	double getResolution();
	bool isLoaded();
	string getPdbCode();	
	float getDensity(int C, int R, int S);
	VectorThree getNearestPeak(VectorThree XYZ, Interpolator* interp);
	VectorThree getCRSFromXYZ(VectorThree XYZ);
	VectorThree getXYZFromCRS(double c, double r, double s);
    int getPosition(int C, int R, int S);
	VectorThree getCRS(int position);
};



