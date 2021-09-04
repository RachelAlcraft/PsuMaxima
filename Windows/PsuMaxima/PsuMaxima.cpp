// PsuMaxima.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Ccp4.h"

int main()
{
    /******   WINDOWS SPECIFIC SETTINGS  ***************/
    string ccp4directory = "C:/Dev/Github/ProteinDataFiles/ccp4_data/";
    /***************************************************/
    Ccp4 myCcp4("1ejg",ccp4directory);
    std::cout << myCcp4.getPdbCode() << " " << myCcp4.getResolution() << " " << myCcp4.isLoaded() << "\n";
}


