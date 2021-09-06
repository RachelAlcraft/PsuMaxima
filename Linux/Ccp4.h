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
using namespace std;

class Ccp4
{
private:
	double PI;
	bool _loaded;
	string _pdbCode;
	double _resolution;
	//SETINGS
	string _directory;

	//THE "WORDS" from the Ccp4 file
	int _w01_NX;
	int _w02_NY;
	int _w03_NZ;
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
	
	//The matrix data
	vector<float> _matrix;
	vector<pair<float,int> > _matrixPeaks;

	//Helper functioms
	int getPosition(int C, int R, int S);
	vector<int> getCRS(int position);
	void calculateOrthoMat(float w11_CELLA_X, float w12_CELLA_Y, float w13_CELLA_Z, float w14_CELLB_X, float w15_CELLB_Y, float w16_CELLB_Z);
	void calculateOrigin(int w05_NXSTART, int w06_NYSTART, int w07_NZSTART, int w17_MAPC, int w18_MAPR, int w19_MAPS);

public:
	Ccp4(string pdbCode, string directory);
	double getResolution();
	bool isLoaded();
	string getPdbCode();
	void makePeaks(PdbFile* pdbFile);
	float getDensity(int C, int R, int S);
	VectorThree getCRS(double x, double y, double z);
	VectorThree getXYZ(double c, double r, double s);
};



