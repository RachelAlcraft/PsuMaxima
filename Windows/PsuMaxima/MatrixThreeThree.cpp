/*
* 3x3 Matrix class
*  0 1 2
*  3 4 5
*  6 7 8
*/
#include "MatrixThreeThree.h"

MatrixThreeThree::MatrixThreeThree()
{
    for (int i = 0; i < 9; ++i)
    {
        _matrix.push_back(0);
    }
}

MatrixThreeThree::MatrixThreeThree(vector<double> vals)
{
    for (int i = 0; i < 9; ++i)
    {
        _matrix.push_back(vals[i]);
    }
}

MatrixThreeThree MatrixThreeThree::getInverse()
{
    double detWhole = getDeterminant();
    vector<double> transp;
    transp.push_back(_matrix[0]);
    transp.push_back(_matrix[3]);
    transp.push_back(_matrix[6]);
    transp.push_back(_matrix[1]);
    transp.push_back(_matrix[4]);
    transp.push_back(_matrix[7]);
    transp.push_back(_matrix[2]);
    transp.push_back(_matrix[5]);
    transp.push_back(_matrix[8]);

    MatrixThreeThree transpose(transp);
    MatrixThreeThree matinverse;

    int factor = 1;

    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            double thisValue = transpose.getValue(i, j);
            double detReduced = transpose.getInnerDeterminant(i, j);
            matinverse.putValue(detReduced * factor / detWhole, i, j);
            factor *= -1;
        }
    }
    return matinverse;

}

double MatrixThreeThree::getDeterminant()
{
    int factor = -1;
    double det = 0;
    for (int i = 0; i < 3; ++i)
    {
        factor = factor * -1;
        double row_val = _matrix[3 * i];
        double newdet = getInnerDeterminant(i, 0);
        det = det + (factor * row_val * newdet);
    }
    return det;
}

double MatrixThreeThree::getInnerDeterminant(int col, int row)
{
    vector<double> smallMat;
    if (col == 0)
    {
        if (row != 0)
        {
            smallMat.push_back(_matrix[1]);
            smallMat.push_back(_matrix[2]);
        }
        if (row != 1)
        {
            smallMat.push_back(_matrix[4]);
            smallMat.push_back(_matrix[5]);
        }
        if (row != 2)
        {
            smallMat.push_back(_matrix[7]);
            smallMat.push_back(_matrix[8]);
        }
    }
    else if (col == 1)
    {
        if (row != 0)
        {
            smallMat.push_back(_matrix[0]);
            smallMat.push_back(_matrix[2]);
        }
        if (row != 1)
        {
            smallMat.push_back(_matrix[3]);
            smallMat.push_back(_matrix[5]);
        }
        if (row != 2)
        {
            smallMat.push_back(_matrix[6]);
            smallMat.push_back(_matrix[8]);
        }
    }
    else// (col == 1)
    {
        if (row != 0)
        {
            smallMat.push_back(_matrix[0]);
            smallMat.push_back(_matrix[1]);
        }
        if (row != 1)
        {
            smallMat.push_back(_matrix[3]);
            smallMat.push_back(_matrix[4]);
        }
        if (row != 2)
        {
            smallMat.push_back(_matrix[6]);
            smallMat.push_back(_matrix[7]);
        }
    }

    double n11 = smallMat[0];
    double n12 = smallMat[1];
    double n21 = smallMat[2];
    double n22 = smallMat[3];

    return n11 * n22 - n12 * n21;
}

double MatrixThreeThree::getValue(int col, int row)
{
    int pos = row * 3 + col;
    return _matrix[pos];
}

void MatrixThreeThree::putValue(double val, int col, int row)
{
    int pos = row * 3 + col;
    _matrix[pos] = val;
}

VectorThree MatrixThreeThree::multiply(VectorThree col)
{
    //So, this is by row not by column, or,,, anyway which is which...
    double col0 = col.A;
    double col1 = col.B;
    double col2 = col.C;

    VectorThree scaled;

    double s0 = col0 * _matrix[0];
    double s1 = col0 * _matrix[1];
    double s2 = col0 * _matrix[2];

    s0 += col1 * _matrix[3];
    s1 += col1 * _matrix[4];
    s2 += col1 * _matrix[5];

    s0 += col2 * _matrix[6];
    s1 += col2 * _matrix[7];
    s2 += col2 * _matrix[8];

    scaled.putByIndex(0, s0);
    scaled.putByIndex(1, s1);
    scaled.putByIndex(2, s2);

    return scaled;
}
