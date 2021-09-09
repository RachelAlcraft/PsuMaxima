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
