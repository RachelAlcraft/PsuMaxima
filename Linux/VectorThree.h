#pragma once

#include <string>

class VectorThree
{
public:
	double A;
	double B;
	double C;
    bool Valid;
	double getByIndex(int idx);
	void putByIndex(int idx, double val);
    VectorThree();
    VectorThree(bool isValid);
    VectorThree(double a, double b, double c);
    double distance(VectorThree ABC);
    double getMagnitude();
    double getDotProduct(VectorThree vec);
    VectorThree operator + (VectorThree const& obj);
    VectorThree operator - (VectorThree const& obj);
    double getAngle(VectorThree vec);
    std::string getKey();
};

