#include "Interpolator.h"

Interpolator::Interpolator(vector<float> matrix, int i, int j, int k)
{
	Matrix = matrix;
	Fastest = i;
	Middle = j;
	Slowest = k;
}
