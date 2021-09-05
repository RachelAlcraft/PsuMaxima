// PsuMaxima.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Ccp4.h"

int main()
{
    /******   COMMAND LINE INPUTS  ***************/
    string COMMAND = "PEAKS";
    /***************************************************/
    /******   WINDOWS SPECIFIC SETTINGS  ***************/
    string ccp4directory = "C:/Dev/Github/ProteinDataFiles/ccp4_data/";
    /***************************************************/
    Ccp4 myCcp4("1ejg", ccp4directory);
    if (COMMAND == "PEAKS")
    {
        myCcp4.makePeaks();
    }
    

}


