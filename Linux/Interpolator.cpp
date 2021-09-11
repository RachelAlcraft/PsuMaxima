#include "Interpolator.h"

// ****** ABSTRACT CLASS ****************************************
Interpolator::Interpolator(vector<float> matrix, int x, int y, int z)
{
	Matrix = matrix;
	XLen = x;
	YLen = y;
	ZLen = z;
    h = 0.01;
}

float Interpolator::getExactValue(int x, int y, int z)
{
    int sliceSize = XLen * YLen;
    int pos = z * sliceSize;
    pos += XLen * y;
    pos += x;
    if (pos > 0 && pos < Matrix.size())
        return Matrix[pos];
    else
        return 0;
}

double Interpolator::getRadiant(double x, double y, double z)
{    
    double val = getValue(x, y, z);
    double dx = (getValue(x + h, y, z) - val) / h;
    double dy = (getValue(x, y + h, z) - val) / h;
    double dz = (getValue(x, y, z + h) - val) / h;
    double radiant = (abs(dx) + abs(dy) + abs(dz)) / 3;
    return radiant;
}

double Interpolator::getLaplacian(double x, double y, double z)
{	
    double val = getValue(x, y, z);
    double xx = getDxDx(x, y, z, val);
    double yy = getDyDy(x, y, z, val);
    double zz = getDzDz(x, y, z, val);
    return xx + yy + zz;
}

double Interpolator::getDxDx(double x, double y, double z, double val)
{    
    double va = getValue(x - h, y, z);
    double vb = getValue(x + h, y, z);
    double dd = (va + vb - 2 * val) / (h * h);
    return dd;
}
double Interpolator::getDyDy(double x, double y, double z, double val)
{    
    double va = getValue(x, y - h, z);
    double vb = getValue(x, y + h, z);
    double dd = (va + vb - 2 * val) / (h * h);
    return dd;
}
double Interpolator::getDzDz(double x, double y, double z, double val)
{    
    double va = getValue(x, y, z - h);
    double vb = getValue(x, y, z + h);
    double dd = (va + vb - 2 * val) / (h * h);
    return dd;
}

// ****** Nearest Neighbour Implementation ****************************************
Nearest::Nearest(vector<float> matrix, int x, int y, int z):Interpolator(matrix,x,y,z)
{
}

double Nearest::getValue(double x, double y, double z)
{
    int i = int(x);
    int j = int(y);
    int k = int(z);
    return getExactValue(i, j, k);
}
// ****** Nearest Neighbour Implementation ****************************************

// ****** Thevenaz Spline Convolution Implementation ****************************************
// Thévenaz, Philippe, Thierry Blu, and Michael Unser. ‘Image Interpolation and Resampling’, n.d., 39.
//   http://bigwww.epfl.ch/thevenaz/interpolation/
// *******************************************************************************
Thevenaz::Thevenaz(vector<float> matrix, int x, int y, int z):Interpolator(matrix, x, y, z)
{
}

double Thevenaz::getValue(double x, double y, double z)
{
	return 0.0;
}
