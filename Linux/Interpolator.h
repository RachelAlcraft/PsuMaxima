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
	int XLen;
	int YLen;
	int ZLen;
	double h;
public:	
	Interpolator(vector<float> matrix, int x, int y, int z);	
	virtual double getValue(double x, double y, double z) = 0;
	float getExactValue(int x, int y, int z);
	double getRadiant(double x, double y, double z);
	double getLaplacian(double x, double y, double z);			
	double getDxDx(double x, double y, double z, double val);
	double getDyDy(double x, double y, double z, double val);
	double getDzDz(double x, double y, double z, double val);
};

class Nearest :public Interpolator
{
public:	
	Nearest(vector<float> matrix, int x, int y, int z);
	double getValue(double x, double y, double z);	
};

class Thevenaz:public Interpolator
{
protected:		
	Thevenaz(vector<float> matrix, int x, int y, int z);
	double getValue(double x, double y, double z);	

};