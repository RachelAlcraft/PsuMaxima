#pragma once
class VectorThree
{
public:
	double A;
	double B;
	double C;
	double getByIndex(int idx);
	void putByIndex(int idx, double val);
    VectorThree();
    VectorThree(double a, double b, double c);
};

