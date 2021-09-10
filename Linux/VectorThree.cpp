
#include <cmath>

#include "VectorThree.h"

VectorThree::VectorThree()
{
    A = 0;
    B = 0;
    C = 0;
}


VectorThree::VectorThree(double a, double b, double c)
{
    A = a;
    B = b;
    C = c;
}

double VectorThree::getByIndex(int idx)
{
    if (idx == 0)
        return A;
    else if (idx == 1)
        return B;
    else // (idx == 0)
        return C;
}

void VectorThree::putByIndex(int idx, double val)
{
    if (idx == 0)
        A = val;
    else if (idx == 1)
        B = val;
    else // (idx == 0)
        C = val;
}

double VectorThree::getMagnitude()
{    
	double mag = (A*A)+(B*B)+(C*C);
	return sqrt(mag);
}
VectorThree VectorThree::operator+(VectorThree const& obj)
{
	A += obj.A;
	B += obj.B;
	C += obj.C;
	return VectorThree(A, B, C);
}
VectorThree VectorThree::operator-(VectorThree const& obj)
{
	A -= obj.A;
	B -= obj.B;
	C -= obj.C;
	return VectorThree(A, B, C);
}
double VectorThree::getAngle(VectorThree vec)
{
    VectorThree BA(0-A,0-B,0-C);
    VectorThree BC(0-vec.A,0-vec.B,0-vec.C);
    double dot = BA.getDotProduct(BC);
    double magBA = BA.getMagnitude();
    double magBC = BC.getMagnitude();
    double cosTheta = dot / (magBA * magBC);
    double theta = acos(cosTheta);    
    return theta; //in radians
}

double VectorThree::getDotProduct(VectorThree vec)
{
            double px = A * vec.A;
            double py = B * vec.B;
            double pz = C * vec.C;
            return px + py + pz;
}
