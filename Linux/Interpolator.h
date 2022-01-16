#pragma once
/************************************************************************
* RSA Created 11.9.21
* RSA Last updated 16.01.22
* 
* Abstract class Interpolator
* Implementation Nearest: a simple nearest neighbour implementation
* Implementation Thevenaz: a beta slpine implemnentation taken from http://bigwww.epfl.ch/thevenaz/interpolation/
* Implementation Algorithm: not really interpolation but calculating each point theoretically using the IAM model:
*	References for IAM:		https://phenix-online.org/phenixwebsite_static/mainsite/files/presentations/latest/pavel_maps_2.pdf (p.7)
							https://github.com/project-gemmi/gemmi/blob/master/include/gemmi/dencalc.hpp  
							https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Modules_and_Websites_(Inorganic_Chemistry)/Crystallography/X-rays/CromerMann_coefficients
           

* This class implements different algorithms for interpolation. It is written for an electron density matrix
* and this class mostly has no knowledge of this and is pure interpolation, with the exception of the Algorithm implementation
* This could be improved such that the algorithm class could implement a function from elsewhere.
* 
* Outside of this interpolation class the electron density needs a firther transformation 
* from lattice space to real space, but that does not concern the interpolator.
* 
* The interpolator primarily returns values and derivatives. 
* getRadiant is the first derivative, which is the l1 norm of del, the sum of the absolute values fo the first partial derivatives
* getLaplacian is the more standard second derivative, the sum of the second partial derivatives
* 
************************************************************************/

#include <string>
#include <vector>

#include "Atom.h"

using namespace std;
class Interpolator
{
protected:
	vector<float> Matrix;
	int XLen;
	int YLen;
	int ZLen;
	double h;
public:	
	Interpolator(vector<float> matrix, int x, int y, int z);	
	void addMatrix(vector<float> matrix, int x, int y, int z);
	virtual double getValue(double x, double y, double z) = 0;
	float getExactValue(int x, int y, int z);
	int getSize() { return Matrix.size(); }
	vector<float> getStatsValues();
	vector<int> getStatsPoses();
	int getPosition(int x, int y, int z);
	double getRadiant(double x, double y, double z);
	double getLaplacian(double x, double y, double z);			
	double getDxDx(double x, double y, double z, double val);
	double getDyDy(double x, double y, double z, double val);
	double getDzDz(double x, double y, double z, double val);
	VectorThree getNearbyAtomPeak(VectorThree XYZ, bool density);
	VectorThree getNearbyGridPeak(VectorThree XYZ, bool density);	
	virtual void addAtoms(vector<Atom> atoms) {}
	virtual void createBondElectrons() {}

protected:
	VectorThree getNearestPeakRecursive(VectorThree Orig, VectorThree XYZ, bool density, int level, double width, int cap, bool invalidNonConvergence);
};

class Nearest :public Interpolator
{
public:	
	Nearest(vector<float> matrix, int x, int y, int z);
	double getValue(double x, double y, double z);	
};

class Thevenaz:public Interpolator
{
public:
	Thevenaz(vector<float> matrix, int x, int y, int z);
	double getValue(double x, double y, double z);	
protected:
	// member data
	double TOLERANCE;
	int _degree;
	vector<double> _coefficients;

	// Internal functions
	void createCoefficients();
	vector<double> getPole(int degree);
	vector<double> getRow3d(int y, int z, int length);	
	void putRow3d(int y, int z, vector<double> row, int length);	
	vector<double> getColumn3d(int x, int z, int length);	
	void putColumn3d(int x, int z, vector<double> col, int length);
	vector<double> getHole3d(int x, int y, int length);	
	void putHole3d(int x, int y, vector<double> bore, int length);
	vector<double> convertToInterpolationCoefficients(vector<double> pole, int numPoles, int width, vector<double> row);
	double InitialCausalCoefficient(vector<double> c, long dataLength, double pole);
	double InitialAntiCausalCoefficient(vector<double> c, long dataLength, double pole);
	vector<double> applyValue3(double val, vector<int> idc, int weight_length);
	vector<double> applyValue5(double val, vector<int> idc, int weight_length);
	vector<double> applyValue7(double val, vector<int> idc, int weight_length);
	vector<double> applyValue9(double val, vector<int> idc, int weight_length);
	

};

class Algorithmic :public Interpolator
{
public:
	Algorithmic();
	double getValue(double x, double y, double z);
	//specific to this interpolator class
	void addAtoms(vector<Atom> atoms);
	void createBondElectrons();

private:
	vector<Atom> _atoms;

};