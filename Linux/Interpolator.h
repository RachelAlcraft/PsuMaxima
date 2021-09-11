#pragma once
/************************************************************************
* RSA 11.9.21
************************************************************************/

#include <string>
#include <vector>

using namespace std;
class Interpolator
{
protected:
	vector<float> Matrix;
	int Fastest;
	int Middle;
	int Slowest;
public:
	//virtual GeoCoords applyTransformation(GeoCoords point) { return GeoCoords(0, 0, 0); }; //won't let me =0 it ??? TODO
	Interpolator(vector<float> matrix, int i, int j, int k);	
	virtual double getValue(double i, double j, double k) = 0;
	virtual double getRadiant(double i, double j, double k) = 0;
	virtual double getLaplacian(double i, double j, double k) = 0;	

	
	
protected:


};